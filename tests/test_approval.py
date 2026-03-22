"""Tests for the approval flow."""

import os
import sys
import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.database import init_db, insert_draft, get_draft
from backend.approval.approval_manager import approve, reject, get_queue
from backend.approval.sms_approval import handle_sms_reply


@pytest.fixture(autouse=True)
def setup_db(tmp_path, monkeypatch):
    import backend.database as db_module
    db_path = tmp_path / "test.db"
    monkeypatch.setattr(db_module, "DB_PATH", db_path)
    db_module._connection = None
    init_db()
    yield
    db_module.close_db()


def _create_test_draft():
    return insert_draft(
        agent="leads",
        draft_text="Hi, thanks for reaching out!",
        recipient_name="Test Person",
        recipient_phone="555-0000",
    )


def test_approve_draft():
    draft_id = _create_test_draft()
    result = approve(draft_id)
    assert result["status"] == "approved"
    draft = get_draft(draft_id)
    assert draft["status"] == "approved"
    assert draft["approved_at"] is not None


def test_approve_with_edits():
    draft_id = _create_test_draft()
    result = approve(draft_id, edited_text="Edited version!")
    assert result["status"] == "approved"
    draft = get_draft(draft_id)
    assert draft["owner_edits"] == "Edited version!"


def test_reject_draft():
    draft_id = _create_test_draft()
    result = reject(draft_id)
    assert result["status"] == "rejected"
    draft = get_draft(draft_id)
    assert draft["status"] == "rejected"


def test_cannot_approve_already_approved():
    draft_id = _create_test_draft()
    approve(draft_id)
    result = approve(draft_id)
    assert "error" in result


def test_get_queue():
    _create_test_draft()
    _create_test_draft()
    queue = get_queue()
    assert len(queue) == 2


def test_sms_approve():
    draft_id = _create_test_draft()
    response = handle_sms_reply("+15551234567", f"A-{draft_id}")
    assert "APPROVED" in response
    draft = get_draft(draft_id)
    assert draft["status"] == "approved"


def test_sms_reject():
    draft_id = _create_test_draft()
    response = handle_sms_reply("+15551234567", f"R-{draft_id}")
    assert "REJECTED" in response


def test_sms_invalid_format():
    response = handle_sms_reply("+15551234567", "hello")
    assert "Didn't understand" in response


def test_approve_nonexistent():
    result = approve(9999)
    assert "error" in result
