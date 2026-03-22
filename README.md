# AI Business with Automated Agents

A plug-and-play system that lets one person run an entire business using AI agents as automated employees. Configure it for **any** business type — pressure washing, law firm, dentist, landscaping, restaurant, real estate — change one config file and the agents adapt.

**Live Demo (Website):** https://seang1121.github.io/ai-business-with-automated-agents

---

## How It Works

```
                         business_config.yaml
                                |
                    +-----------+-----------+
                    |                       |
              Phase 1: WEBSITE        Phase 2: AI AGENTS
              (index.html)            (Python backend)
                    |                       |
            Customer finds you      6 agents run your ops
            on Google, calls        +-----------------------+
                    |               | Leads Agent           |
                    +---> Form ---> | Estimating Agent      |
                          Submit    | Scheduling Agent      |
                                    | Reviews Agent         |
                                    | Finance Agent         |
                                    | Marketing Agent       |
                                    +-----------+-----------+
                                                |
                                          APPROVAL QUEUE
                                                |
                                    Owner approves/edits/rejects
                                                |
                                          Message sent
```

---

## The Six Agents

| Agent | Trigger | What It Does |
|-------|---------|-------------|
| **Leads** | New form submission | Drafts personalized follow-up within minutes |
| **Estimating** | Lead with address + service | Calculates ballpark price range |
| **Scheduling** | Lead ready to book | Suggests available time slots |
| **Reviews** | Job marked complete | Drafts thank-you + Google review request |
| **Finance** | Job complete + price agreed | Generates professional invoice |
| **Marketing** | Manual trigger | Drafts social media posts with hashtags |

**Core rule:** Agents draft, you approve. Nothing sends without your say-so.

---

## Quick Start

```bash
# Clone
git clone https://github.com/seang1121/ai-business-with-automated-agents.git
cd ai-business-with-automated-agents

# Run (Windows)
start.bat

# Run (Mac/Linux)
chmod +x start.sh && ./start.sh
```

The launcher creates a venv, installs dependencies, seeds demo data, and starts the server.

**Dashboard:** http://localhost:5000/dashboard/ (PIN: `123456`)

---

## Demo Mode vs Live Mode

| | Demo Mode | Live Mode |
|---|---|---|
| **API keys needed?** | No | Yes (Claude, Twilio) |
| **AI responses** | Realistic mocks from templates | Real Claude API calls |
| **SMS/Email** | Logged to console | Actually sent via Twilio |
| **Dashboard** | Fully functional | Fully functional |
| **Config** | `mode: "demo"` | `mode: "live"` |

Demo mode works out of the box. Switch to live mode by adding API keys to `.env` and setting `mode: "live"` in `business_config.yaml`.

---

## Configure for Any Business

Edit `business_config.yaml` — that's the only file you need to change.

**Pressure Washing (default):**
```yaml
business:
  name: "Example Pressure Washing Co."
  type: "pressure_washing"
  services:
    - name: "Driveway Cleaning"
      starting_price: 150
```

**Law Firm:**
```yaml
business:
  name: "Smith & Associates Law"
  type: "family_law"
  services:
    - name: "Divorce & Separation"
      starting_price: 500
      unit: "consultation"
```

**Dental Office:**
```yaml
business:
  name: "Bright Smile Dental"
  type: "dental"
  services:
    - name: "Teeth Cleaning"
      starting_price: 150
      unit: "per visit"
```

The agents automatically adapt their tone, terminology, and behavior based on the business type. No code changes required.

### Ready-to-Use Examples

Full configs for 6 business types are in the `examples/` folder. Copy any one into `business_config.yaml` to try it:

| Example | File | Business Type |
|---------|------|--------------|
| Pressure Washing | `examples/` (default config) | Home services |
| Law Firm | `examples/law-firm.yaml` | Professional services |
| Dental Office | `examples/dental-office.yaml` | Healthcare |
| Real Estate | `examples/real-estate.yaml` | Sales / brokerage |
| Restaurant / Catering | `examples/restaurant.yaml` | Food & hospitality |
| Auto Detailing | `examples/auto-detailing.yaml` | Mobile services |
| Landscaping | `examples/landscaping.yaml` | Seasonal services |

```bash
# Try the law firm example:
cp examples/law-firm.yaml business_config.yaml
python backend/app.py
```

Each example includes realistic services, pricing, hours, agent tone settings, tax rates, and social media hashtags for that industry.

---

## Project Structure

```
ai-business-with-automated-agents/
|
|-- index.html                  # Phase 1: Business website (HTML/CSS/JS)
|-- style.css                   # Mobile-first responsive styles
|-- script.js                   # Mobile menu, smooth scroll
|-- business_config.yaml        # THE SINGLE CONFIG FILE
|-- requirements.txt            # Python dependencies
|-- start.bat / start.sh        # One-command launchers
|-- .env.example                # API key template
|
|-- backend/
|   |-- app.py                  # Flask entry point + API routes
|   |-- config.py               # Config loader + validator
|   |-- database.py             # SQLite singleton wrapper
|   |-- schema.sql              # Database tables
|   |-- mode.py                 # Demo/Live mode logic
|   |-- seed_demo.py            # Seeds realistic demo data
|   |-- cli.py                  # Terminal dashboard alternative
|   |
|   |-- agents/                 # The six AI agents
|   |   |-- base_agent.py       # Abstract base (draft-approve-send pattern)
|   |   |-- leads_agent.py
|   |   |-- scheduling_agent.py
|   |   |-- reviews_agent.py
|   |   |-- finance_agent.py
|   |   |-- marketing_agent.py
|   |   |-- estimating_agent.py
|   |
|   |-- services/               # External service wrappers
|   |   |-- claude_service.py   # Claude API + demo mocks
|   |   |-- twilio_service.py   # SMS + demo logging
|   |   |-- notification.py     # Owner alert routing
|   |
|   |-- approval/               # Approval queue system
|   |   |-- approval_manager.py # Approve/reject/edit drafts
|   |   |-- sms_approval.py     # Twilio SMS reply handler
|   |
|   |-- dashboard/              # Owner web dashboard
|   |   |-- routes.py           # Flask blueprint
|   |   |-- templates/          # Jinja2 HTML templates
|   |   |-- static/             # CSS + JS
|   |
|   |-- integrations/           # Third-party integrations
|       |-- openclaw_integration.py  # OpenClaw AI assistant
|
|-- examples/                   # Ready-to-use configs for 6+ business types
|-- tests/                      # Test suite
|-- project-docs/               # Architecture documentation
```

---

## CLI Usage

```bash
python backend/cli.py status     # System overview
python backend/cli.py drafts     # List pending drafts
python backend/cli.py approve 1  # Approve draft #1
python backend/cli.py reject 2   # Reject draft #2
python backend/cli.py leads      # List all leads
python backend/cli.py activity   # Recent activity log
python backend/cli.py demo       # Seed demo data + show status
```

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/webhook/formspree` | Receive form submissions |
| POST | `/api/webhook/twilio` | SMS approval replies |
| GET | `/api/agents/status` | All agent statuses |
| POST | `/api/drafts/{id}/approve` | Approve a draft |
| POST | `/api/drafts/{id}/reject` | Reject a draft |
| POST | `/api/jobs/{id}/complete` | Mark job complete |
| POST | `/api/leads/{id}/book` | Book a lead |
| POST | `/api/marketing/generate` | Trigger marketing agent |

---

## OpenClaw Integration

[OpenClaw](https://openclaw.com) is an AI executive assistant that can operate a computer, browse the web, and manage tasks. This repo includes an integration that lets OpenClaw act as a conversational layer on top of the agent system:

- **Approval Relay** — OpenClaw presents drafts conversationally and handles approvals via chat
- **Proactive Monitoring** — Alerts you about stale leads and unapproved drafts
- **Browser Testing** — Verifies your website works end-to-end
- **Multi-Channel Dispatch** — Sends approved messages via Telegram, Discord, etc.

Enable in `business_config.yaml`:
```yaml
integrations:
  openclaw:
    enabled: true
    gateway_url: "ws://127.0.0.1:18789"
```

---

## Tech Stack

| Component | Technology |
|-----------|-----------|
| Website | HTML + CSS + Vanilla JS (zero dependencies) |
| Backend | Python + Flask |
| Database | SQLite (zero setup) |
| AI | Claude API (Anthropic) |
| SMS | Twilio |
| Dashboard | Flask + Jinja2 + CSS |
| Config | YAML (with comments) |
| AI Assistant | OpenClaw (optional) |

---

## Roadmap

| Phase | Status | What It Unlocks |
|-------|--------|----------------|
| Phase 1 — Website | Complete | Online presence, inbound leads, local SEO |
| Phase 2 — AI Agents | Complete | Automated follow-up, scheduling, invoicing, marketing |
| Phase 3 — Growth | Planned | Online self-booking, seasonal outreach, referral tracking |

---

*Built with Claude Code.*
