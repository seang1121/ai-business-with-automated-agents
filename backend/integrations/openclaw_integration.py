"""
OpenClaw Integration — AI Executive Assistant Layer

OpenClaw (https://openclaw.com) is an AI executive assistant platform that can
operate a computer, browse the web, manage tasks, and act as a persistent agent
with memory. It connects via a local WebSocket gateway.

This integration shows how OpenClaw can sit on top of the agent system as a
conversational relay — presenting drafts to the owner naturally, handling
approvals via chat, and proactively monitoring the business pipeline.

INTEGRATION POINTS:
1. Approval Relay — OpenClaw receives new draft notifications via the gateway,
   presents them to the owner conversationally ("Hey, a new lead came in from
   John Smith. Here's the draft follow-up. Should I approve it?"), and calls
   the approval API based on the owner's response.

2. Proactive Monitoring — OpenClaw periodically checks the dashboard API for
   stale leads (no response in X hours) or unapproved drafts, and nudges the
   owner: "You have 3 drafts waiting for approval. Want me to show them?"

3. Browser Testing — OpenClaw can visit the business website, fill out the
   contact form with test data, and verify the webhook pipeline works end-to-end.

4. Multi-Channel Dispatch — After a draft is approved, OpenClaw can send the
   message via channels it supports natively (Telegram, Discord, etc.) in
   addition to or instead of SMS/email.

SETUP:
1. Install OpenClaw: https://openclaw.com/docs/install
2. Start the gateway: openclaw gateway --port 18789
3. Set in .env:
   OPENCLAW_GATEWAY_URL=ws://127.0.0.1:18789
   OPENCLAW_GATEWAY_TOKEN=your-token
4. Enable in business_config.yaml:
   integrations.openclaw.enabled: true
"""

import os
import json
import logging
from backend.config import BusinessConfig

log = logging.getLogger(__name__)


class OpenClawIntegration:
    """Connects to the OpenClaw gateway for conversational business management."""

    def __init__(self, config: BusinessConfig):
        self.config = config
        oc_config = config.integrations.get("openclaw", {})
        self.enabled = oc_config.get("enabled", False)
        self.gateway_url = os.environ.get(
            "OPENCLAW_GATEWAY_URL",
            oc_config.get("gateway_url", "ws://127.0.0.1:18789")
        )
        self.token = os.environ.get("OPENCLAW_GATEWAY_TOKEN", "")
        self.features = oc_config.get("features", [])
        self._ws = None

    async def connect(self) -> bool:
        """Connect to the OpenClaw gateway via WebSocket."""
        if not self.enabled:
            log.info("[OpenClaw] Integration disabled in config.")
            return False

        if self.config.is_demo:
            log.info(f"[OpenClaw DEMO] Would connect to {self.gateway_url}")
            return True

        try:
            import websockets
            self._ws = await websockets.connect(
                self.gateway_url,
                additional_headers={"Authorization": f"Bearer {self.token}"},
            )
            log.info(f"[OpenClaw] Connected to gateway at {self.gateway_url}")
            return True
        except Exception as e:
            log.error(f"[OpenClaw] Failed to connect: {e}")
            return False

    async def send_draft_notification(self, draft: dict) -> None:
        """Send a new draft to OpenClaw for conversational approval."""
        if "approval_relay" not in self.features:
            return

        message = {
            "type": "draft_notification",
            "draft_id": draft.get("id"),
            "agent": draft.get("agent"),
            "recipient": draft.get("recipient_name"),
            "preview": draft.get("draft_text", "")[:200],
            "actions": ["approve", "reject", "edit"],
        }

        if self.config.is_demo:
            log.info(f"[OpenClaw DEMO] Would send draft notification: {json.dumps(message, indent=2)}")
            return

        if self._ws:
            await self._ws.send(json.dumps(message))
            log.info(f"[OpenClaw] Draft #{draft.get('id')} sent to gateway.")

    async def check_stale_items(self, pending_drafts: list, stale_leads: list) -> None:
        """Proactively alert owner about items needing attention."""
        if "proactive_monitoring" not in self.features:
            return

        alerts = []
        if pending_drafts:
            alerts.append(
                f"You have {len(pending_drafts)} draft(s) waiting for approval."
            )
        if stale_leads:
            alerts.append(
                f"You have {len(stale_leads)} lead(s) with no response yet."
            )

        if not alerts:
            return

        message = {
            "type": "proactive_alert",
            "alerts": alerts,
            "pending_count": len(pending_drafts),
            "stale_count": len(stale_leads),
        }

        if self.config.is_demo:
            log.info(f"[OpenClaw DEMO] Proactive alert: {json.dumps(message, indent=2)}")
            return

        if self._ws:
            await self._ws.send(json.dumps(message))

    async def run_browser_test(self, website_url: str) -> dict:
        """Ask OpenClaw to visit the website and verify it loads correctly."""
        if "browser_testing" not in self.features:
            return {"status": "skipped", "reason": "browser_testing not enabled"}

        message = {
            "type": "browser_test",
            "url": website_url,
            "checks": [
                "page_loads",
                "phone_number_visible",
                "form_present",
                "no_console_errors",
            ],
        }

        if self.config.is_demo:
            log.info(f"[OpenClaw DEMO] Would run browser test on {website_url}")
            return {
                "status": "demo",
                "url": website_url,
                "checks_passed": ["page_loads", "phone_number_visible",
                                   "form_present", "no_console_errors"],
                "checks_failed": [],
            }

        if self._ws:
            await self._ws.send(json.dumps(message))
            # In production, would await response from gateway
            return {"status": "sent", "url": website_url}

        return {"status": "error", "reason": "Not connected to gateway"}

    async def disconnect(self) -> None:
        """Disconnect from the gateway."""
        if self._ws:
            await self._ws.close()
            self._ws = None
            log.info("[OpenClaw] Disconnected from gateway.")


def create_openclaw_integration(config: BusinessConfig) -> OpenClawIntegration:
    """Factory function for creating the integration."""
    return OpenClawIntegration(config)
