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

## How Agents Adapt by Business Type

Every agent reads `business_config.yaml` at runtime — the business name, type, services, tone, and settings all flow into the AI prompts and mock templates automatically. Here's what changes across industries:

### Leads Agent

The leads agent drafts a follow-up message when someone submits the contact form. The **tone** and **language** change completely based on the business type:

| Business | Config Setting | Example Draft |
|----------|---------------|---------------|
| Pressure Washing | `response_tone: "friendly and professional"` | *"Hi Mike, thanks for reaching out! We'd love to help with your driveway cleaning. I'll follow up shortly to schedule a free estimate."* |
| Law Firm | `response_tone: "empathetic, professional, and reassuring"` | *"Hi Maria, thank you for reaching out to Smith & Associates. We understand this is a difficult time. Sarah Smith, Esq. will personally contact you to discuss your divorce consultation in complete confidence."* |
| Dental Office | `response_tone: "warm, professional, and calming"` | *"Hi Jennifer, thanks for contacting Bright Smile Dental! Dr. Chen specializes in making every visit comfortable, especially for patients who are nervous. We'll reach out to schedule your cleaning."* |
| Restaurant | `response_tone: "warm, inviting, and enthusiastic about food"` | *"Hi Tom, thank you for your interest in catering! Marco would love to discuss your wedding reception. We'll be in touch soon to talk menu options and guest count."* |

**What drives the difference:** The `response_tone` field is injected directly into the Claude prompt. The agent also pulls the owner name, service list, and area from config so the message sounds hyper-local and personal.

### Estimating Agent

The estimating agent calculates a price range using `starting_price` from the service list and `size_multipliers` from config:

| Business | Service | Base Price | Small (1.0x) | Medium (1.5x) | Large (2.2x) |
|----------|---------|-----------|-------------|---------------|-------------|
| Pressure Washing | Driveway Cleaning | $150 | $150 | $225 | $330 |
| Law Firm | Divorce Consultation | $500 | $500 | $1,000 | $1,750 |
| Dental | Dental Implants | $3,000 | $3,000 | $3,900 | $5,400 |
| Auto Detailing | Ceramic Coating | $500 | $500 | $650 | $800 |

**What drives the difference:** Each business defines its own `size_multipliers` in config. A law firm's "large" multiplier (3.5x) is much bigger than a pressure washer's (2.2x) because case complexity varies more than driveway size. The unit labels also change — "per job" vs "consultation" vs "per implant."

### Scheduling Agent

The scheduling agent reads `hours` and `slot_duration_minutes` from config:

| Business | Hours | Slot Duration | Buffer |
|----------|-------|---------------|--------|
| Pressure Washing | Mon-Sat 7AM-7PM | 60 min | 30 min between jobs |
| Law Firm | Mon-Fri 9AM-5PM | 30 min | 15 min between appointments |
| Dental | Mon-Sat 8AM-6PM | 30 min | 15 min between patients |
| Restaurant | Tue-Sun (closed Mon) | 120 min | 60 min between events |
| Landscaping | Mon-Sat 6:30AM-6PM | 60 min | 45 min (travel time) |

**What drives the difference:** A dentist needs 30-minute slots with 15-minute turnover. A restaurant books 2-hour event windows. A landscaper starts at 6:30 AM. The scheduling agent reads all of this from config and never suggests a Sunday slot for a law firm or a Monday slot for a restaurant.

### Reviews Agent

The reviews agent drafts a thank-you + Google review request after job completion:

| Business | Delay After Completion | Example Draft |
|----------|----------------------|---------------|
| Pressure Washing | 2 hours | *"Hi Susan, your siding looks amazing! If you have a sec, a quick Google review helps your neighbors find us."* |
| Law Firm | 24 hours | *"Thank you for trusting Smith & Associates with your custody case. If you felt well-represented, a review helps other families in similar situations find compassionate counsel."* |
| Dental | 4 hours | *"Hi James, we hope your cleaning went smoothly! If you had a positive experience, a Google review helps other patients who might be nervous about the dentist."* |
| Restaurant | 12 hours | *"Hi Linda, it was an honor to cater your wedding! If the food brought joy to your day, a quick review helps other couples discover Nonna's Kitchen."* |

**What drives the difference:** `delay_after_completion_hours` controls when the review request fires. A law firm waits 24 hours (sensitivity of the matter). A pressure washer sends within 2 hours (while the clean driveway is still exciting). The tone in the prompt adapts to match — empathetic for legal, enthusiastic for food.

### Finance Agent

The finance agent generates invoices using business-specific tax rates and payment methods:

| Business | Tax Rate | Payment Methods | Invoice Prefix |
|----------|----------|----------------|---------------|
| Pressure Washing | 8.625% (NY) | Cash, Venmo, Check, Credit Card | INV |
| Law Firm | 0% (exempt) | Check, Credit Card, Wire Transfer | SFA |
| Dental | 0% (medical exempt) | Insurance, Credit Card, CareCredit, Cash | BSD |
| Restaurant | 8.875% (NY + Westchester) | Credit Card, Cash, Venmo, Check | NK |
| Auto Detailing | 8.25% (TX) | Cash, Venmo, Zelle, Credit Card | APX |

**What drives the difference:** `tax_rate` and `payment_methods` are in config. Legal and medical services are tax-exempt. A dental office lists "Insurance" and "CareCredit" as payment options. A Texas auto detailer uses the TX rate. The invoice prefix creates numbering like `SFA-1001` (law firm) vs `APX-1001` (auto detailing).

### Marketing Agent

The marketing agent drafts social media posts using platform-specific settings:

| Business | Platforms | Hashtags |
|----------|----------|----------|
| Pressure Washing | Facebook, Instagram | #localbusiness #beforeandafter |
| Law Firm | LinkedIn, Facebook | #familylaw #divorceattorney #nassaucounty #legalhelp |
| Dental | Instagram, Facebook | #dentist #brightersmile #brooklyndentist #cosmeticdentistry |
| Restaurant | Instagram, Facebook, TikTok | #italianfood #catering #westchestereats #foodie |
| Real Estate | Instagram, Facebook, TikTok | #miamirealestate #homesearch #dreamhome #justlisted |
| Landscaping | Facebook, Instagram, NextDoor | #landscaping #lawncare #curbappeal #greenthumb |

**What drives the difference:** A law firm posts on LinkedIn (professional audience). A restaurant targets TikTok and Instagram (visual food content). A landscaper uses NextDoor (hyperlocal neighborhood network). The hashtags are industry-specific and location-tagged.

### Summary: What Each Config Field Controls

| Config Field | Which Agents Use It | What Changes |
|-------------|--------------------|----|
| `business.name` | All 6 | Business name in every draft |
| `business.type` | All 6 | Industry context in AI prompts |
| `business.owner_name` | All 6 | Sign-off name on messages |
| `business.services[]` | Leads, Estimating, Finance | Service names, pricing, categories |
| `business.hours` | Scheduling | Available time slots |
| `business.slot_duration_minutes` | Scheduling | Appointment length |
| `business.google_review_link` | Reviews | Link in review request |
| `agents.leads.response_tone` | Leads | AI prompt tone instruction |
| `agents.scheduling.slots_to_suggest` | Scheduling | Number of options offered |
| `agents.reviews.delay_after_completion_hours` | Reviews | When review request fires |
| `agents.finance.tax_rate` | Finance | Tax calculation on invoices |
| `agents.finance.payment_methods` | Finance | Listed on invoices |
| `agents.marketing.platforms` | Marketing | Which social networks to target |
| `agents.marketing.hashtags` | Marketing | Tags appended to posts |
| `agents.estimating.size_multipliers` | Estimating | Price range calculation |

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
