"""Agent registry — loads all six agents."""

from backend.agents.leads_agent import LeadsAgent
from backend.agents.scheduling_agent import SchedulingAgent
from backend.agents.reviews_agent import ReviewsAgent
from backend.agents.finance_agent import FinanceAgent
from backend.agents.marketing_agent import MarketingAgent
from backend.agents.estimating_agent import EstimatingAgent

AGENT_CLASSES = {
    "leads": LeadsAgent,
    "scheduling": SchedulingAgent,
    "reviews": ReviewsAgent,
    "finance": FinanceAgent,
    "marketing": MarketingAgent,
    "estimating": EstimatingAgent,
}


def create_agents(config, claude_service, notification_service) -> dict:
    """Instantiate all agents and return a name->agent dict."""
    agents = {}
    for name, cls in AGENT_CLASSES.items():
        agents[name] = cls(config, claude_service, notification_service)
    return agents


def get_agent_names() -> list[str]:
    return list(AGENT_CLASSES.keys())
