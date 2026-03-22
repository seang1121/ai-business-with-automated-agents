"""Claude API wrapper with demo mock fallback."""

import os
import logging
from backend.config import BusinessConfig

log = logging.getLogger(__name__)

# Mock response templates keyed by agent name.
# Each uses {business_name}, {owner_name}, {customer_name}, {service}, etc.
MOCK_TEMPLATES = {
    "leads": (
        "Hi {customer_name}, thank you for reaching out to {business_name}! "
        "We'd love to help with your {service} needs. {owner_name} will personally "
        "follow up with you shortly to discuss your project and provide a free estimate. "
        "Looking forward to working with you!"
    ),
    "scheduling": (
        "Hi {customer_name}, great news! We have the following times available "
        "for your {service}:\n\n"
        "1. Monday at 9:00 AM\n"
        "2. Wednesday at 2:00 PM\n"
        "3. Friday at 10:00 AM\n\n"
        "Which works best for you? Just reply with your preferred time and "
        "we'll get you on the calendar. — {owner_name}"
    ),
    "reviews": (
        "Hi {customer_name}, thank you so much for choosing {business_name} "
        "for your {service}! We hope everything looks great. If you have a moment, "
        "we'd truly appreciate a quick review — it helps other neighbors find us.\n\n"
        "{review_link}\n\n"
        "Thank you again! — {owner_name}"
    ),
    "finance": (
        "INVOICE #{invoice_number}\n"
        "From: {business_name}\n"
        "To: {customer_name}\n"
        "Date: {date}\n\n"
        "Service: {service}\n"
        "Subtotal: ${subtotal:.2f}\n"
        "Tax: ${tax:.2f}\n"
        "Total: ${total:.2f}\n\n"
        "Payment methods: {payment_methods}\n"
        "Thank you for your business!"
    ),
    "marketing": (
        "Another job well done! We just completed a {service} project "
        "and the results speak for themselves. Swipe to see the before & after!\n\n"
        "Serving {regions} with pride.\n"
        "Call {phone} for your free estimate.\n\n"
        "{hashtags}"
    ),
    "estimating": (
        "Hi {customer_name}, based on your {service} request at {address}, "
        "here's our preliminary estimate:\n\n"
        "Estimated range: ${low_estimate:.0f} - ${high_estimate:.0f}\n\n"
        "This is a ballpark based on typical jobs in your area. {owner_name} "
        "will confirm the exact price after a quick on-site look (free, no obligation). "
        "Want to schedule a visit?"
    ),
}


class ClaudeService:
    def __init__(self, config: BusinessConfig):
        self.config = config
        self.client = None
        if config.is_live:
            try:
                import anthropic
                self.client = anthropic.Anthropic(
                    api_key=os.environ["ANTHROPIC_API_KEY"]
                )
            except ImportError:
                log.error("anthropic package not installed. Run: pip install anthropic")
                raise

    def generate_draft(self, agent_name: str, prompt: str, context: dict) -> str:
        """Generate a draft using Claude API (live) or mock templates (demo)."""
        if self.config.is_demo:
            return self._mock_response(agent_name, context)

        response = self.client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1024,
            messages=[{"role": "user", "content": prompt}],
        )
        return response.content[0].text

    def _mock_response(self, agent_name: str, context: dict) -> str:
        """Return a realistic mock response using templates + business config."""
        template = MOCK_TEMPLATES.get(agent_name, "Draft for {customer_name}")
        biz = self.config.business

        # Build merge dict with safe defaults
        merge = {
            "business_name": biz.get("name", "Your Business"),
            "owner_name": biz.get("owner_name", "The Owner"),
            "phone": biz.get("phone", "(555) 000-0000"),
            "regions": ", ".join(biz.get("service_area", {}).get("regions", [])),
            "review_link": biz.get("google_review_link", "https://g.page/review"),
            "hashtags": " ".join(
                self.config.agents.get("marketing", {}).get("hashtags", [])
            ),
            "payment_methods": ", ".join(
                self.config.agents.get("finance", {}).get("payment_methods", ["Cash"])
            ),
        }
        merge.update(context)

        try:
            return template.format(**merge)
        except KeyError as e:
            log.warning(f"Mock template missing key {e} for agent {agent_name}")
            return template.format_map(SafeDict(merge))


class SafeDict(dict):
    """Returns placeholder for missing keys instead of raising KeyError."""
    def __missing__(self, key):
        return f"[{key}]"
