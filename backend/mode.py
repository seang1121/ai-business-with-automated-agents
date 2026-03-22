"""Demo vs Live mode utilities."""


def is_demo(config) -> bool:
    return config.mode == "demo"


def mode_banner(config) -> str:
    if config.is_demo:
        return (
            "DEMO MODE — No real messages will be sent. "
            "Mock AI responses are used. Set mode: 'live' in "
            "business_config.yaml and add API keys to .env for production."
        )
    return "LIVE MODE — Real API calls active. Messages will be sent after approval."
