"""Tests for config loading and validation."""

import os
import sys
import tempfile
import pytest
import yaml

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pathlib import Path
from backend.config import load_config, BusinessConfig


def _write_config(tmp_path, data):
    path = tmp_path / "test_config.yaml"
    with open(path, "w") as f:
        yaml.dump(data, f)
    return path


def test_load_valid_config(tmp_path):
    config_data = {
        "business": {
            "name": "Test Biz",
            "type": "test",
            "owner_name": "Tester",
            "phone": "555-1234",
            "email": "test@test.com",
            "services": [{"name": "Test Service", "starting_price": 100}],
        },
        "agents": {"leads": {"enabled": True}},
        "mode": "demo",
    }
    path = _write_config(tmp_path, config_data)
    config = load_config(path)
    assert isinstance(config, BusinessConfig)
    assert config.business["name"] == "Test Biz"
    assert config.is_demo is True
    assert config.is_live is False


def test_get_service_by_name(tmp_path):
    config_data = {
        "business": {
            "name": "Test", "type": "test", "owner_name": "T",
            "phone": "555", "email": "t@t.com",
            "services": [
                {"name": "Driveway Cleaning", "starting_price": 150},
                {"name": "Roof Washing", "starting_price": 350},
            ],
        },
        "mode": "demo",
    }
    path = _write_config(tmp_path, config_data)
    config = load_config(path)
    svc = config.get_service_by_name("Driveway Cleaning")
    assert svc is not None
    assert svc["starting_price"] == 150
    assert config.get_service_by_name("nonexistent") is None


def test_missing_business_section(tmp_path):
    path = _write_config(tmp_path, {"mode": "demo"})
    with pytest.raises(SystemExit):
        load_config(path)


def test_missing_required_fields(tmp_path):
    config_data = {
        "business": {
            "name": "Test",
            # Missing type, owner_name, phone, email
            "services": [{"name": "X"}],
        },
        "mode": "demo",
    }
    path = _write_config(tmp_path, config_data)
    with pytest.raises(SystemExit):
        load_config(path)
