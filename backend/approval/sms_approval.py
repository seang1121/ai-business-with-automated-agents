"""SMS-based approval handler for Twilio webhook replies."""

import re
import logging
from backend.approval import approval_manager
from backend import database as db

log = logging.getLogger(__name__)


def handle_sms_reply(from_number: str, body: str) -> str:
    """
    Parse owner's SMS reply and approve/reject the referenced draft.

    Expected formats:
        A-47    -> Approve draft #47
        R-47    -> Reject draft #47
        A 47    -> Approve draft #47
        R 47    -> Reject draft #47
    """
    body = body.strip().upper()

    # Try to parse "A-47" or "R-47" pattern
    match = re.match(r"^([AR])[\s\-]?(\d+)$", body)
    if not match:
        return (
            "Didn't understand that. Reply with:\n"
            "A-{id} to approve\n"
            "R-{id} to reject"
        )

    action = match.group(1)
    draft_id = int(match.group(2))

    draft = db.get_draft(draft_id)
    if not draft:
        return f"Draft #{draft_id} not found."
    if draft["status"] != "pending":
        return f"Draft #{draft_id} is already {draft['status']}."

    if action == "A":
        result = approval_manager.approve(draft_id)
        return f"Draft #{draft_id} APPROVED and queued for delivery."
    else:
        result = approval_manager.reject(draft_id)
        return f"Draft #{draft_id} REJECTED."
