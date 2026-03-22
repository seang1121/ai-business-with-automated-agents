"""Flask entry point — webhooks, API routes, dashboard."""

import os
import sys
import logging

from flask import Flask, request, jsonify, redirect, url_for

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.config import load_config
from backend.database import init_db
from backend.mode import mode_banner
from backend.services.claude_service import ClaudeService
from backend.services.twilio_service import TwilioService
from backend.services.notification import NotificationService
from backend.agents import create_agents, get_agent_names
from backend.approval import approval_manager
from backend.approval.sms_approval import handle_sms_reply
from backend.dashboard.routes import dashboard_bp

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
log = logging.getLogger(__name__)


def create_app():
    """Application factory."""
    config = load_config()
    init_db()

    app = Flask(__name__)
    app.secret_key = os.environ.get("FLASK_SECRET_KEY", "dev-secret-change-me")

    # Store config and services on app for access in routes
    app.config["biz_config"] = config

    claude_svc = ClaudeService(config)
    twilio_svc = TwilioService(config)
    notify_svc = NotificationService(config, twilio_svc)
    agents = create_agents(config, claude_svc, notify_svc)

    app.config["agents"] = agents
    app.config["claude_service"] = claude_svc
    app.config["twilio_service"] = twilio_svc

    # Register dashboard blueprint
    app.register_blueprint(dashboard_bp)

    # --- Root redirect ---
    @app.route("/")
    def index():
        return redirect(url_for("dashboard.dashboard_home"))

    # --- Webhook: Formspree form submission ---
    @app.route("/api/webhook/formspree", methods=["POST"])
    def webhook_formspree():
        data = request.json or request.form.to_dict()
        log.info(f"[WEBHOOK] Form submission received: {data.get('name', 'unknown')}")

        results = {}

        # Trigger leads agent
        leads = agents.get("leads")
        if leads and leads.enabled:
            draft_id = leads.trigger(data)
            results["leads"] = {"draft_id": draft_id}

        # Trigger estimating agent (if service + address present)
        estimating = agents.get("estimating")
        if estimating and estimating.enabled and data.get("service") and data.get("address"):
            # Pass the lead_id from leads agent
            if results.get("leads", {}).get("draft_id"):
                from backend import database as db
                # Get the lead that was just created
                pending = db.get_pending_drafts()
                if pending:
                    data["lead_id"] = pending[0].get("lead_id")
            draft_id = estimating.trigger(data)
            results["estimating"] = {"draft_id": draft_id}

        return jsonify({"status": "ok", "agents_triggered": results})

    # --- Webhook: Twilio SMS reply ---
    @app.route("/api/webhook/twilio", methods=["POST"])
    def webhook_twilio():
        from_number = request.form.get("From", "")
        body = request.form.get("Body", "")
        response_text = handle_sms_reply(from_number, body)
        return f"<Response><Message>{response_text}</Message></Response>", 200, {
            "Content-Type": "text/xml"
        }

    # --- API: Agent status ---
    @app.route("/api/agents/status")
    def agents_status():
        status = {}
        for name in get_agent_names():
            agent = agents.get(name)
            status[name] = {
                "enabled": agent.enabled if agent else False,
                "config": agent.agent_config if agent else {},
            }
        return jsonify(status)

    # --- API: Draft actions ---
    @app.route("/api/drafts/<int:draft_id>/approve", methods=["POST"])
    def api_approve_draft(draft_id):
        edited = request.json.get("edited_text") if request.json else None
        result = approval_manager.approve(draft_id, edited)
        return jsonify(result)

    @app.route("/api/drafts/<int:draft_id>/reject", methods=["POST"])
    def api_reject_draft(draft_id):
        reason = request.json.get("reason", "") if request.json else ""
        result = approval_manager.reject(draft_id, reason)
        return jsonify(result)

    # --- API: Job actions ---
    @app.route("/api/jobs/<int:job_id>/complete", methods=["POST"])
    def api_complete_job(job_id):
        from backend.database import complete_job, get_job
        complete_job(job_id)
        results = {}

        # Trigger reviews agent
        reviews = agents.get("reviews")
        if reviews and reviews.enabled:
            draft_id = reviews.trigger({"job_id": job_id})
            results["reviews"] = {"draft_id": draft_id}

        # Trigger finance agent
        finance = agents.get("finance")
        if finance and finance.enabled:
            draft_id = finance.trigger({"job_id": job_id})
            results["finance"] = {"draft_id": draft_id}

        return jsonify({"status": "ok", "agents_triggered": results})

    # --- API: Lead booking ---
    @app.route("/api/leads/<int:lead_id>/book", methods=["POST"])
    def api_book_lead(lead_id):
        from backend.database import update_lead_status
        update_lead_status(lead_id, "ready_to_book")
        results = {}

        scheduling = agents.get("scheduling")
        if scheduling and scheduling.enabled:
            draft_id = scheduling.trigger({"lead_id": lead_id})
            results["scheduling"] = {"draft_id": draft_id}

        return jsonify({"status": "ok", "agents_triggered": results})

    # --- API: Marketing trigger ---
    @app.route("/api/marketing/generate", methods=["POST"])
    def api_marketing_generate():
        data = request.json or {}
        job_id = data.get("job_id")
        if not job_id:
            return jsonify({"error": "job_id required"}), 400

        marketing = agents.get("marketing")
        if marketing and marketing.enabled:
            draft_id = marketing.trigger({"job_id": job_id})
            return jsonify({"status": "ok", "draft_id": draft_id})
        return jsonify({"error": "Marketing agent disabled"}), 400

    log.info(f"\n{'='*60}")
    log.info(f"  {config.business.get('name', 'AI Business')} — Agent Backend")
    log.info(f"  {mode_banner(config)}")
    log.info(f"  Dashboard: http://localhost:5000/dashboard/")
    log.info(f"{'='*60}\n")

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5000, debug=True)
