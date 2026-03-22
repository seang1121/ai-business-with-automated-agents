"""Dashboard blueprint — owner views drafts, approves, manages leads."""

import os
from functools import wraps

from flask import (
    Blueprint, render_template, request, redirect,
    url_for, session, flash, jsonify, current_app,
)

from backend import database as db
from backend.approval import approval_manager
from backend.mode import mode_banner

dashboard_bp = Blueprint(
    "dashboard", __name__,
    url_prefix="/dashboard",
    template_folder="templates",
    static_folder="static",
    static_url_path="/dashboard/static",
)


def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get("authenticated"):
            return redirect(url_for("dashboard.login"))
        return f(*args, **kwargs)
    return decorated


@dashboard_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        pin = request.form.get("pin", "")
        expected = os.environ.get("DASHBOARD_PIN", "123456")
        if pin == expected:
            session["authenticated"] = True
            return redirect(url_for("dashboard.dashboard_home"))
        flash("Invalid PIN. Try again.")
    return render_template("login.html")


@dashboard_bp.route("/logout")
def logout():
    session.pop("authenticated", None)
    return redirect(url_for("dashboard.login"))


@dashboard_bp.route("/")
@login_required
def dashboard_home():
    config = current_app.config["biz_config"]
    stats = db.get_stats()
    pending = db.get_pending_drafts()
    recent = db.get_all_drafts(limit=10)
    activity = db.get_activity_log(limit=15)
    return render_template(
        "dashboard.html",
        config=config,
        stats=stats,
        pending=pending,
        recent=recent,
        activity=activity,
        mode_banner=mode_banner(config),
    )


@dashboard_bp.route("/drafts/<int:draft_id>")
@login_required
def draft_detail(draft_id):
    config = current_app.config["biz_config"]
    draft = db.get_draft(draft_id)
    if not draft:
        flash("Draft not found.")
        return redirect(url_for("dashboard.dashboard_home"))
    return render_template("draft_detail.html", draft=draft, config=config)


@dashboard_bp.route("/drafts/<int:draft_id>/approve", methods=["POST"])
@login_required
def approve_draft(draft_id):
    edited = request.form.get("edited_text")
    approval_manager.approve(draft_id, edited if edited else None)
    flash(f"Draft #{draft_id} approved.")
    return redirect(url_for("dashboard.dashboard_home"))


@dashboard_bp.route("/drafts/<int:draft_id>/reject", methods=["POST"])
@login_required
def reject_draft(draft_id):
    approval_manager.reject(draft_id)
    flash(f"Draft #{draft_id} rejected.")
    return redirect(url_for("dashboard.dashboard_home"))


@dashboard_bp.route("/leads")
@login_required
def leads_view():
    config = current_app.config["biz_config"]
    leads = db.get_all_leads()
    return render_template("leads.html", leads=leads, config=config)


@dashboard_bp.route("/leads/<int:lead_id>/book", methods=["POST"])
@login_required
def book_lead(lead_id):
    db.update_lead_status(lead_id, "ready_to_book")
    agents = current_app.config["agents"]
    scheduling = agents.get("scheduling")
    if scheduling and scheduling.enabled:
        scheduling.trigger({"lead_id": lead_id})
    flash(f"Lead #{lead_id} moved to booking. Scheduling agent triggered.")
    return redirect(url_for("dashboard.leads_view"))
