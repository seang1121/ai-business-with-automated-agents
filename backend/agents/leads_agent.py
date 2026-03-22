"""Leads Agent — responds to new form submissions with personalized follow-up."""

from backend.agents.base_agent import BaseAgent
from backend import database as db


class LeadsAgent(BaseAgent):
    AGENT_NAME = "leads"

    def trigger(self, payload: dict) -> int | None:
        """Triggered by a new form submission (Formspree webhook)."""
        # Store the lead
        lead_id = db.insert_lead(
            name=payload.get("name", ""),
            phone=payload.get("phone", ""),
            email=payload.get("email", ""),
            service=payload.get("service", ""),
            address=payload.get("address", ""),
            notes=payload.get("notes", ""),
            call_time=payload.get("call_time", ""),
        )
        payload["lead_id"] = lead_id
        payload["customer_name"] = payload.get("name", "Customer")
        return self.create_draft(payload, lead_id=lead_id)

    def build_prompt(self, payload: dict) -> str:
        biz = self._biz()
        tone = self.agent_config.get("response_tone", "friendly and professional")
        return (
            f"You are a helpful assistant for {biz['name']}, a {biz['type']} business "
            f"owned by {biz['owner_name']} in "
            f"{', '.join(biz.get('service_area', {}).get('regions', []))}.\n\n"
            f"Services offered: {self._services_list()}\n\n"
            f"A new lead just submitted a contact form:\n"
            f"- Name: {payload.get('name', 'Unknown')}\n"
            f"- Service interested in: {payload.get('service', 'Not specified')}\n"
            f"- Address: {payload.get('address', 'Not provided')}\n"
            f"- Notes: {payload.get('notes', 'None')}\n"
            f"- Preferred call time: {payload.get('call_time', 'Any time')}\n\n"
            f"Draft a {tone} follow-up message (2-3 sentences) thanking them for "
            f"reaching out, confirming we serve their area, and suggesting next steps. "
            f"Keep it personal and conversational. Sign as {biz['owner_name']}."
        )
