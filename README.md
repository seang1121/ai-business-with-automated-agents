# AI Business with Automated Agents

A complete local service business website with a built-in roadmap for AI-powered automated agents that handle leads, scheduling, reviews, invoicing, marketing, and estimating — so one person can run an entire business.

**Live Demo:** https://seang1121.github.io/ai-business-with-automated-agents

---

## What This Is

A production-ready website template for any local service business (pressure washing, landscaping, HVAC, plumbing, cleaning — anything), paired with an AI agent architecture that automates the operational side of the business.

**Phase 1 — The Website (Complete)**
A conversion-optimized, mobile-first marketing site. A customer finds you on Google, sees the phone number, and calls. That's the entire funnel.

**Phase 2 — Automated AI Agents (Planned)**
Six AI agents that act as your automated employees — drafting follow-ups, scheduling jobs, requesting reviews, generating invoices, posting to social media, and calculating estimates. Every agent drafts and waits for owner approval before anything goes out.

**Phase 3 — Scale (Future)**
Online self-booking, seasonal outreach, referral tracking, job photo archives, and multi-crew scheduling.

---

## The Six Agents

| Agent | Trigger | What It Does |
|-------|---------|-------------|
| **Leads Agent** | New form submission | Drafts personalized follow-up within minutes |
| **Scheduling Agent** | Lead ready to book | Suggests time slots from your calendar |
| **Reviews Agent** | Job marked complete | Drafts thank-you + Google review request |
| **Finance Agent** | Job complete, price agreed | Generates professional invoice |
| **Marketing Agent** | Good before/after photos | Drafts social media posts with captions |
| **Estimating Agent** | New lead with address | Calculates ballpark estimate by service + property |

**Core principle:** Agents draft, you approve. Nothing sends without your say-so.

---

## Tech Stack

### Phase 1 (Website)
Plain HTML + CSS + Vanilla JS — zero dependencies, zero build step, opens in any browser offline. Hosted free on GitHub Pages.

```
ai-business-with-automated-agents/
├── index.html         # Full single-page site
├── style.css          # Mobile-first responsive styles
├── script.js          # Mobile menu, smooth scroll, sticky header
├── README.md          # This file
├── BUSINESS-PLAN.txt  # Full roadmap + setup checklist
└── images/            # Before/after photos go here
```

### Phase 2 (Agents — Planned)
- **Claude API** — agent reasoning and message drafting
- **Formspree webhooks** — form submission triggers
- **Twilio** — SMS approval flow for the owner
- **SQLite or Airtable** — job and lead logging
- **Approval UI** — owner approves/edits/rejects with one tap

---

## Quick Start

1. Clone this repo
2. Open `index.html` — search and replace all `[bracketed placeholders]` with your real info
3. Replace `(555) 000-0000` with your phone number everywhere
4. Replace `info@yourbusiness.com` with your email
5. Add your before/after photos to `images/`
6. Set up [Formspree](https://formspree.io) and replace `YOUR_FORMSPREE_ID`
7. Deploy: drag the folder to [netlify.com/drop](https://app.netlify.com/drop) or push to GitHub Pages

See `BUSINESS-PLAN.txt` for the full setup checklist and detailed instructions.

---

## Design Principles

- **Elderly & mobile-friendly:** min 20px text, 48x48px tap targets, no confusing animations
- **Phone number is king:** visible in sticky header on every scroll position, every device
- **High contrast:** Navy/Orange/White, WCAG AA throughout
- **SEO built-in:** LocalBusiness JSON-LD, meta tags, semantic HTML, town name lists
- **Agent-ready forms:** clean field names (`name`, `phone`, `email`, `service`, `address`) ready for webhook automation

---

## Use This Template For

- Pressure washing
- Landscaping / lawn care
- HVAC / plumbing / electrical
- House cleaning / maid service
- Roofing / gutters
- Auto detailing
- Pool service
- Any local service business

Just swap the service names, photos, and pricing — the structure works for any trade.

---

## Business Model Summary

| Phase | Status | What It Unlocks |
|-------|--------|----------------|
| Phase 1 — Website | Complete | Online presence, inbound leads, local SEO, credibility |
| Phase 2 — AI Agents | Planned | Faster response, consistent follow-up, less manual work per job |
| Phase 3 — Growth Tools | Future | Scale operations without proportional headcount increase |

---

*Built with Claude Code.*
