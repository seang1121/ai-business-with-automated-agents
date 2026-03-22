"""Owner notification dispatch."""

import logging
from backend.config import BusinessConfig

log = logging.getLogger(__name__)


class NotificationService:
    def __init__(self, config: BusinessConfig, twilio_service=None):
        self.config = config
        self.twilio = twilio_service
        self.method = config.notifications.get("method", "dashboard_only")

    def send_owner_alert(self, message: str) -> None:
        """Notify the business owner about a new draft or event."""
        log.info(f"[NOTIFICATION] {message}")

        if self.method == "sms" and self.twilio:
            owner_phone = self.config.notifications.get("owner_phone")
            if owner_phone:
                self.twilio.send_sms(owner_phone, message)
        elif self.method == "email":
            # Email integration placeholder — Resend, SendGrid, etc.
            owner_email = self.config.notifications.get("owner_email")
            log.info(f"[EMAIL] Would send to {owner_email}: {message}")
        # dashboard_only: no external notification, owner checks dashboard
