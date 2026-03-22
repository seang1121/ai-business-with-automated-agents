"""Reviews Agent — sends thank-you + Google review request after job completion."""

from backend.agents.base_agent import BaseAgent
from backend import database as db


class ReviewsAgent(BaseAgent):
    AGENT_NAME = "reviews"

    def trigger(self, payload: dict) -> int | None:
        """Triggered when a job is marked complete."""
        job = db.get_job(payload["job_id"])
        if not job:
            return None

        lead = db.get_lead(job["lead_id"]) if job.get("lead_id") else {}
        if not lead:
            lead = {}

        payload["customer_name"] = lead.get("name", "Valued Customer")
        payload["service"] = job.get("service", "your service")
        payload["phone"] = lead.get("phone", "")
        payload["email"] = lead.get("email", "")
        payload["review_link"] = self._biz().get(
            "google_review_link", "https://g.page/review"
        )

        return self.create_draft(payload, job_id=payload["job_id"],
                                 lead_id=job.get("lead_id"))

    def build_prompt(self, payload: dict) -> str:
        biz = self._biz()
        return (
            f"You are a customer follow-up assistant for {biz['name']}, "
            f"a {biz['type']} business.\n\n"
            f"A job was just completed:\n"
            f"- Customer: {payload.get('customer_name')}\n"
            f"- Service: {payload.get('service')}\n\n"
            f"Draft a warm, personal thank-you message (2-3 sentences) that:\n"
            f"1. Thanks them for choosing {biz['name']}\n"
            f"2. References the specific service they received\n"
            f"3. Asks them to leave a Google review at: {payload.get('review_link')}\n\n"
            f"Keep it genuine, not salesy. Sign as {biz['owner_name']}."
        )
