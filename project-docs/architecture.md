# Architecture — AI Business with Automated Agents

## System Overview

```
CUSTOMER                    OWNER                     SYSTEM
  |                           |                         |
  |  Visits website           |                         |
  |  Fills contact form       |                         |
  |  ----POST----->           |                         |
  |                     Formspree webhook               |
  |                           |                         |
  |                     /api/webhook/formspree           |
  |                           |                         |
  |                     +-----v-------+                 |
  |                     | Leads Agent |-- creates lead  |
  |                     +-----+-------+   in SQLite     |
  |                           |                         |
  |                     +-----v-----------+             |
  |                     | Estimating Agent|-- if service |
  |                     +-----+-----------+   + address |
  |                           |                         |
  |                     Both agents create DRAFTS       |
  |                           |                         |
  |                     +-----v-----------+             |
  |                     | APPROVAL QUEUE  |             |
  |                     | (SQLite drafts) |             |
  |                     +-----+-----------+             |
  |                           |                         |
  |                     Owner notified                  |
  |                     (dashboard / SMS / OpenClaw)     |
  |                           |                         |
  |                     Owner reviews draft             |
  |                     APPROVE / EDIT / REJECT         |
  |                           |                         |
  |                     If approved:                    |
  |  <--- SMS/Email ---  Message sent to customer       |
  |                           |                         |
```

## Agent Lifecycle

Every agent follows the same pattern (enforced by `BaseAgent`):

1. **Trigger** — An event occurs (form submission, job complete, etc.)
2. **Build Prompt** — Agent constructs a Claude prompt using business config
3. **Generate Draft** — Claude API (live) or mock template (demo) creates text
4. **Store Draft** — Draft saved to SQLite with status `pending`
5. **Notify Owner** — Owner alerted via configured method
6. **Await Approval** — Owner approves, edits, or rejects
7. **Execute** — If approved, message is sent to customer

## Config-Driven Design

All agent behavior is driven by `business_config.yaml`. The agents never hardcode
business-specific content. Instead, they read:

- Business name, type, and owner from `business.`
- Service list and pricing from `business.services[]`
- Hours and scheduling rules from `business.hours`
- Agent-specific settings from `agents.{name}.`
- Notification preferences from `notifications.`

Changing the config file changes the entire system's behavior without touching code.

## Database Schema

- **leads** — Customer contact info from form submissions
- **jobs** — Booked work with dates, prices, status
- **drafts** — Agent-generated text awaiting approval
- **invoices** — Generated invoices with line items and totals
- **activity_log** — Audit trail of all agent actions

## Demo vs Live Mode

The `mode` field in config controls all external service calls:

- `claude_service.py` — Returns mock templates in demo, real API in live
- `twilio_service.py` — Logs to console in demo, sends SMS in live
- `openclaw_integration.py` — Logs messages in demo, connects to gateway in live

This is implemented at the service layer, not the agent layer. Agents don't know
or care which mode they're in — they call the same methods either way.
