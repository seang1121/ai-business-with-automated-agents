"""Estimating Agent — calculates ballpark estimates for new leads."""

from backend.agents.base_agent import BaseAgent
from backend import database as db


class EstimatingAgent(BaseAgent):
    AGENT_NAME = "estimating"

    def trigger(self, payload: dict) -> int | None:
        """Triggered alongside leads agent when a form submission has service + address."""
        if not payload.get("service") or not payload.get("address"):
            return None

        # Calculate estimate range
        low, high = self._calculate_estimate(payload.get("service", ""))
        if low is None:
            return None

        payload["customer_name"] = payload.get("name", "Customer")
        payload["low_estimate"] = low
        payload["high_estimate"] = high

        lead_id = payload.get("lead_id")
        return self.create_draft(payload, lead_id=lead_id)

    def build_prompt(self, payload: dict) -> str:
        biz = self._biz()
        return (
            f"You are the estimating assistant for {biz['name']}, "
            f"a {biz['type']} business.\n\n"
            f"A customer requested an estimate:\n"
            f"- Name: {payload.get('customer_name')}\n"
            f"- Service: {payload.get('service')}\n"
            f"- Address: {payload.get('address')}\n"
            f"- Notes: {payload.get('notes', 'None')}\n\n"
            f"Estimated range: ${payload.get('low_estimate', 0):.0f} - "
            f"${payload.get('high_estimate', 0):.0f}\n\n"
            f"Draft a friendly message presenting this estimate. Emphasize "
            f"that it's a ballpark and {biz['owner_name']} will confirm the exact "
            f"price after a quick look (free, no obligation). "
            f"Sign as {biz['owner_name']}."
        )

    def _calculate_estimate(self, service_name: str) -> tuple[float | None, float | None]:
        """Calculate low/high estimate using base price + size multipliers."""
        svc = self.config.get_service_by_name(service_name)
        if not svc or svc.get("starting_price") is None:
            return None, None

        base = svc["starting_price"]
        multipliers = self.agent_config.get("size_multipliers", {})

        low = base * multipliers.get("small", 1.0)
        high = base * multipliers.get("large", 2.2)
        return low, high
