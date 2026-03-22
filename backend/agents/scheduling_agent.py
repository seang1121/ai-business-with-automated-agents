"""Scheduling Agent — suggests available time slots when a lead is ready to book."""

from datetime import datetime, timedelta

from backend.agents.base_agent import BaseAgent
from backend import database as db


class SchedulingAgent(BaseAgent):
    AGENT_NAME = "scheduling"

    def trigger(self, payload: dict) -> int | None:
        """Triggered when a lead's status changes to ready_to_book."""
        lead = db.get_lead(payload["lead_id"])
        if not lead:
            return None

        payload["customer_name"] = lead["name"]
        payload["service"] = lead.get("service", "your service")
        payload["phone"] = lead.get("phone", "")
        payload["email"] = lead.get("email", "")
        payload["available_slots"] = self._find_open_slots()

        return self.create_draft(payload, lead_id=payload["lead_id"])

    def build_prompt(self, payload: dict) -> str:
        biz = self._biz()
        slots = payload.get("available_slots", [])
        slots_text = "\n".join(f"  {i+1}. {s}" for i, s in enumerate(slots))
        return (
            f"You are the scheduling assistant for {biz['name']}.\n\n"
            f"Customer: {payload.get('customer_name')}\n"
            f"Service requested: {payload.get('service')}\n\n"
            f"Available time slots:\n{slots_text}\n\n"
            f"Draft a friendly message presenting these options to the customer. "
            f"Ask them to pick their preferred time. Keep it short and warm. "
            f"Sign as {biz['owner_name']}."
        )

    def _find_open_slots(self) -> list[str]:
        """Find available slots based on business hours and existing jobs."""
        hours = self._biz().get("hours", {})
        slots_to_suggest = self.agent_config.get("slots_to_suggest", 3)
        buffer = self.agent_config.get("buffer_between_jobs_minutes", 30)
        slot_duration = self._biz().get("slot_duration_minutes", 60)
        found = []
        check_date = datetime.now()

        for _ in range(14):  # Look up to 2 weeks out
            check_date += timedelta(days=1)
            day_name = check_date.strftime("%A").lower()
            day_hours = hours.get(day_name)
            if not day_hours:
                continue

            start_hour, start_min = map(int, day_hours["start"].split(":"))
            end_hour, end_min = map(int, day_hours["end"].split(":"))

            existing_jobs = db.get_jobs_on_date(check_date.strftime("%Y-%m-%d"))
            booked_times = set()
            for job in existing_jobs:
                if job.get("scheduled_time"):
                    booked_times.add(job["scheduled_time"])

            current = check_date.replace(hour=start_hour, minute=start_min)
            end_time = check_date.replace(hour=end_hour, minute=end_min)

            while current + timedelta(minutes=slot_duration) <= end_time:
                time_str = current.strftime("%H:%M")
                if time_str not in booked_times:
                    found.append(
                        f"{check_date.strftime('%A, %B %d')} at {current.strftime('%I:%M %p')}"
                    )
                    if len(found) >= slots_to_suggest:
                        return found
                current += timedelta(minutes=slot_duration + buffer)

        return found if found else ["No slots available in the next 2 weeks — call to arrange."]
