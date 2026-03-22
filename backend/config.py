"""Loads and validates business_config.yaml."""

import os
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml
from dotenv import load_dotenv


CONFIG_PATH = Path(__file__).parent.parent / "business_config.yaml"

REQUIRED_BUSINESS_FIELDS = ["name", "type", "owner_name", "phone", "email"]
REQUIRED_LIVE_ENV = ["ANTHROPIC_API_KEY"]


@dataclass
class BusinessConfig:
    business: dict = field(default_factory=dict)
    agents: dict = field(default_factory=dict)
    mode: str = "demo"
    notifications: dict = field(default_factory=dict)
    integrations: dict = field(default_factory=dict)
    raw: dict = field(default_factory=dict)

    @property
    def is_demo(self) -> bool:
        return self.mode == "demo"

    @property
    def is_live(self) -> bool:
        return self.mode == "live"

    def get_service_by_name(self, name: str) -> dict | None:
        for svc in self.business.get("services", []):
            if svc["name"].lower() == name.lower():
                return svc
        return None

    def get_services_list(self) -> list[str]:
        return [s["name"] for s in self.business.get("services", [])]


def load_config(config_path: Path | None = None) -> BusinessConfig:
    """Load business_config.yaml and .env, validate, return BusinessConfig."""
    path = config_path or CONFIG_PATH

    if not path.exists():
        print(f"ERROR: Config file not found: {path}")
        print("Copy business_config.yaml.example to business_config.yaml and edit it.")
        sys.exit(1)

    with open(path, "r", encoding="utf-8") as f:
        raw = yaml.safe_load(f)

    _validate_config(raw)

    # Load .env
    env_path = Path(__file__).parent.parent / ".env"
    load_dotenv(env_path)

    mode = raw.get("mode", "demo")
    if mode == "live":
        _validate_live_env()

    return BusinessConfig(
        business=raw.get("business", {}),
        agents=raw.get("agents", {}),
        mode=mode,
        notifications=raw.get("notifications", {}),
        integrations=raw.get("integrations", {}),
        raw=raw,
    )


def _validate_config(raw: dict[str, Any]) -> None:
    """Check required fields exist in config."""
    biz = raw.get("business")
    if not biz:
        print("ERROR: 'business' section missing from business_config.yaml")
        sys.exit(1)

    missing = [f for f in REQUIRED_BUSINESS_FIELDS if not biz.get(f)]
    if missing:
        print(f"ERROR: Missing required business fields: {', '.join(missing)}")
        sys.exit(1)

    if not biz.get("services"):
        print("ERROR: No services defined in business_config.yaml")
        sys.exit(1)


def _validate_live_env() -> None:
    """In live mode, ensure API keys are set."""
    missing = [k for k in REQUIRED_LIVE_ENV if not os.environ.get(k)]
    if missing:
        print(f"ERROR: Live mode requires these env vars: {', '.join(missing)}")
        print("Set them in .env or switch to mode: 'demo' in business_config.yaml")
        sys.exit(1)
