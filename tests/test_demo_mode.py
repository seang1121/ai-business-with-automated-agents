"""Tests to verify demo mode doesn't make real API calls."""

import os
import sys
import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.config import load_config
from backend.services.claude_service import ClaudeService
from backend.services.twilio_service import TwilioService


def test_claude_service_demo_no_client():
    config = load_config()
    assert config.is_demo
    svc = ClaudeService(config)
    assert svc.client is None


def test_claude_service_demo_returns_mock():
    config = load_config()
    svc = ClaudeService(config)
    result = svc.generate_draft("leads", "test prompt", {
        "customer_name": "Demo User",
        "service": "Test Service",
    })
    assert isinstance(result, str)
    assert len(result) > 0
    assert "Demo User" in result


def test_twilio_service_demo_no_client():
    config = load_config()
    svc = TwilioService(config)
    assert svc.client is None


def test_twilio_service_demo_logs_instead():
    config = load_config()
    svc = TwilioService(config)
    result = svc.send_sms("+15551234567", "Test message")
    assert result["status"] == "demo"
    assert result["to"] == "+15551234567"


def test_all_mock_templates_have_required_keys():
    """Ensure mock templates don't crash with standard context."""
    from backend.services.claude_service import MOCK_TEMPLATES
    config = load_config()
    svc = ClaudeService(config)

    standard_context = {
        "customer_name": "Test User",
        "service": "Test Service",
        "address": "123 Test St",
        "notes": "None",
        "invoice_number": "INV-0001",
        "subtotal": 100.0,
        "tax": 8.63,
        "total": 108.63,
        "date": "March 1, 2026",
        "low_estimate": 100.0,
        "high_estimate": 220.0,
    }

    for agent_name in MOCK_TEMPLATES:
        result = svc.generate_draft(agent_name, "test", standard_context)
        assert isinstance(result, str)
        assert len(result) > 10, f"Mock for {agent_name} too short: {result}"
