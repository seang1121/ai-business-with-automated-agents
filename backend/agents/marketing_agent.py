"""Marketing Agent — drafts social media posts for completed jobs."""

from backend.agents.base_agent import BaseAgent
from backend import database as db


class MarketingAgent(BaseAgent):
    AGENT_NAME = "marketing"

    def trigger(self, payload: dict) -> int | None:
        """Triggered manually from dashboard for a specific job."""
        job = db.get_job(payload["job_id"])
        if not job:
            return None

        lead = db.get_lead(job["lead_id"]) if job.get("lead_id") else {}
        if not lead:
            lead = {}

        regions = ", ".join(
            self._biz().get("service_area", {}).get("regions", [])
        )
        hashtags = " ".join(self.agent_config.get("hashtags", []))
        platforms = self.agent_config.get("platforms", ["facebook", "instagram"])

        payload["customer_name"] = lead.get("name", "a valued customer")
        payload["service"] = job["service"]
        payload["address"] = job.get("address", lead.get("address", ""))
        payload["regions"] = regions
        payload["hashtags"] = hashtags
        payload["platforms"] = ", ".join(platforms)
        payload["phone"] = self._biz().get("phone", "")

        return self.create_draft(payload, job_id=job["id"])

    def build_prompt(self, payload: dict) -> str:
        biz = self._biz()
        platforms = payload.get("platforms", "social media")
        return (
            f"You are the social media manager for {biz['name']}, "
            f"a {biz['type']} business.\n\n"
            f"A job was just completed:\n"
            f"- Service: {payload.get('service')}\n"
            f"- Location: {payload.get('address', 'local area')}\n\n"
            f"Draft a short, engaging social media post for {platforms}. "
            f"The post should:\n"
            f"1. Highlight the service completed (no customer names)\n"
            f"2. Mention the service area: {payload.get('regions')}\n"
            f"3. Include a call-to-action (call for free estimate)\n"
            f"4. Phone: {biz.get('phone')}\n"
            f"5. End with these hashtags: {payload.get('hashtags')}\n\n"
            f"Keep it under 200 words. Energetic but professional."
        )
