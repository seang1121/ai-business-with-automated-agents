"""Tests for agent draft creation in demo mode."""

import os
import sys
import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.config import load_config
from backend.database import init_db, get_db, get_pending_drafts, get_draft
from backend.services.claude_service import ClaudeService
from backend.services.notification import NotificationService
from backend.agents.leads_agent import LeadsAgent
from backend.agents.estimating_agent import EstimatingAgent
from backend.agents.reviews_agent import ReviewsAgent


@pytest.fixture(autouse=True)
def setup_db(tmp_path, monkeypatch):
    """Use a temp database for each test."""
    import backend.database as db_module
    db_path = tmp_path / "test.db"
    monkeypatch.setattr(db_module, "DB_PATH", db_path)
    # Reset singleton
    db_module._connection = None
    init_db()
    yield
    db_module.close_db()


@pytest.fixture
def config():
    return load_config()


@pytest.fixture
def services(config):
    claude = ClaudeService(config)
    notify = NotificationService(config)
    return claude, notify


def test_leads_agent_creates_draft(config, services):
    claude, notify = services
    agent = LeadsAgent(config, claude, notify)
    draft_id = agent.trigger({
        "name": "Test Customer",
        "phone": "555-1111",
        "email": "test@test.com",
        "service": "Driveway & Walkway Cleaning",
        "address": "123 Test St",
        "notes": "Test note",
        "call_time": "Morning",
    })
    assert draft_id is not None
    draft = get_draft(draft_id)
    assert draft["agent"] == "leads"
    assert draft["status"] == "pending"
    assert "Test Customer" in draft["draft_text"]


def test_estimating_agent_creates_draft(config, services):
    claude, notify = services
    agent = EstimatingAgent(config, claude, notify)
    draft_id = agent.trigger({
        "name": "Price Checker",
        "service": "Driveway & Walkway Cleaning",
        "address": "456 Test Ave",
        "lead_id": None,
    })
    assert draft_id is not None
    draft = get_draft(draft_id)
    assert draft["agent"] == "estimating"
    assert "$" in draft["draft_text"]


def test_estimating_agent_skips_without_address(config, services):
    claude, notify = services
    agent = EstimatingAgent(config, claude, notify)
    result = agent.trigger({
        "name": "No Address",
        "service": "Driveway Cleaning",
        "address": "",
    })
    assert result is None


def test_disabled_agent_skips(config, services):
    claude, notify = services
    agent = LeadsAgent(config, claude, notify)
    agent.enabled = False
    result = agent.create_draft({"name": "Test"})
    assert result is None
