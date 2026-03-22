"""Abstract base class for all business agents."""

import logging
from abc import ABC, abstractmethod

from backend import database as db

log = logging.getLogger(__name__)


class BaseAgent(ABC):
    """All six agents inherit from this. Enforces the draft-approve-send pattern."""

    AGENT_NAME: str = ""

    def __init__(self, config, claude_service, notification_service):
        self.config = config
        self.claude = claude_service
        self.notify = notification_service
        self.agent_config = config.agents.get(self.AGENT_NAME, {})
        self.enabled = self.agent_config.get("enabled", True)

    @abstractmethod
    def trigger(self, payload: dict) -> int | None:
        """
        Called when this agent's trigger event occurs.
        Returns a draft_id if a draft was created, None if skipped.
        """
        pass

    @abstractmethod
    def build_prompt(self, payload: dict) -> str:
        """Build the Claude prompt for this agent's task."""
        pass

    def create_draft(self, payload: dict, lead_id: int | None = None,
                     job_id: int | None = None) -> int:
        """Shared workflow: build prompt -> Claude -> store draft -> notify owner."""
        if not self.enabled:
            log.info(f"[{self.AGENT_NAME}] Agent disabled, skipping.")
            return None

        prompt = self.build_prompt(payload)
        draft_text = self.claude.generate_draft(self.AGENT_NAME, prompt, payload)

        draft_id = db.insert_draft(
            agent=self.AGENT_NAME,
            lead_id=lead_id,
            job_id=job_id,
            draft_text=draft_text,
            recipient_name=payload.get("customer_name", ""),
            recipient_phone=payload.get("phone", ""),
            recipient_email=payload.get("email", ""),
            metadata=payload,
        )

        db.log_activity(self.AGENT_NAME, "draft_created", draft_id,
                        f"Draft created for {payload.get('customer_name', 'unknown')}")

        self.notify.send_owner_alert(
            f"[{self.AGENT_NAME.upper()}] New draft #{draft_id} ready for approval."
        )

        log.info(f"[{self.AGENT_NAME}] Draft #{draft_id} created.")
        return draft_id

    def _biz(self) -> dict:
        """Shortcut to business config."""
        return self.config.business

    def _services_list(self) -> str:
        """Formatted list of services for prompts."""
        return ", ".join(self.config.get_services_list())
