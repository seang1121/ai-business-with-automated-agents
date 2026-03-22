"""Approval queue — approve, reject, edit drafts before they send."""

import logging
from backend import database as db

log = logging.getLogger(__name__)


def approve(draft_id: int, edited_text: str | None = None) -> dict:
    """Approve a pending draft. Optionally replace text with owner's edits."""
    draft = db.get_draft(draft_id)
    if not draft:
        return {"error": "Draft not found"}
    if draft["status"] != "pending":
        return {"error": f"Draft is already {draft['status']}"}

    db.approve_draft(draft_id, edits=edited_text)
    db.log_activity(
        draft["agent"], "approved", draft_id,
        f"Draft #{draft_id} approved" + (" (with edits)" if edited_text else "")
    )
    log.info(f"Draft #{draft_id} approved by owner.")
    return {"status": "approved", "draft_id": draft_id}


def reject(draft_id: int, reason: str = "") -> dict:
    """Reject a pending draft."""
    draft = db.get_draft(draft_id)
    if not draft:
        return {"error": "Draft not found"}
    if draft["status"] != "pending":
        return {"error": f"Draft is already {draft['status']}"}

    db.reject_draft(draft_id)
    db.log_activity(
        draft["agent"], "rejected", draft_id,
        f"Draft #{draft_id} rejected. Reason: {reason or 'none given'}"
    )
    log.info(f"Draft #{draft_id} rejected.")
    return {"status": "rejected", "draft_id": draft_id}


def get_queue() -> list[dict]:
    """Get all pending drafts awaiting approval."""
    return db.get_pending_drafts()


def get_all(limit: int = 50) -> list[dict]:
    """Get recent drafts of any status."""
    return db.get_all_drafts(limit)
