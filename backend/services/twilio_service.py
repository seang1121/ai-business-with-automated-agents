"""Twilio SMS wrapper with demo mock fallback."""

import os
import logging
from backend.config import BusinessConfig

log = logging.getLogger(__name__)


class TwilioService:
    def __init__(self, config: BusinessConfig):
        self.config = config
        self.client = None
        self.from_number = None
        if config.is_live:
            try:
                from twilio.rest import Client
                self.client = Client(
                    os.environ["TWILIO_ACCOUNT_SID"],
                    os.environ["TWILIO_AUTH_TOKEN"],
                )
                self.from_number = os.environ["TWILIO_PHONE_NUMBER"]
            except ImportError:
                log.error("twilio package not installed. Run: pip install twilio")
                raise

    def send_sms(self, to: str, body: str) -> dict:
        """Send an SMS. In demo mode, logs instead of sending."""
        if self.config.is_demo:
            log.info(f"[DEMO SMS] To: {to} | Body: {body[:100]}...")
            return {"status": "demo", "to": to, "body": body}

        message = self.client.messages.create(
            body=body,
            from_=self.from_number,
            to=to,
        )
        log.info(f"SMS sent to {to}: SID={message.sid}")
        return {"status": "sent", "sid": message.sid, "to": to}
