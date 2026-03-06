# Hamptons Elite Powerwashing

**Live Website:** https://seang1121.github.io/hamptons-elite-powerwashing
**Repo:** https://github.com/seang1121/hamptons-elite-powerwashing

---

## The Business

**Hamptons Elite Powerwashing** is a pressure washing company serving residential homeowners and commercial property owners across Nassau and Suffolk County, Long Island, NY. Services include driveway cleaning, house washing, deck restoration, roof soft washing, commercial building exteriors, and more.

The brand is built on three pillars: **local trust**, **veteran ownership**, and **fast response**. Market research shows that 78% of local service searches convert within 24 hours — the business that responds first wins the job. Everything we build is designed around that insight.

---

## Phase 1 — Website (Complete)

### What We Built

A professional, conversion-optimized marketing website. No apps to download, no accounts to create — a customer finds us on Google, sees the phone number, and calls. That's the entire funnel.

**Sections on the site:**
- Sticky header with phone number always visible on every scroll position, every device
- Hero with primary phone CTA and secondary callback form link
- Full service list — residential (with starting prices) and commercial
- Why Choose Us trust tiles — insured, local, veteran-owned, free estimates, satisfaction guarantee
- Before/after photo gallery (4 pairs — the #1 trust builder in local services)
- Customer testimonials tied to Google reviews
- Callback request form — captures leads from customers who can't call right now
- Service area section listing every Nassau & Suffolk town — boosts local search ranking
- About / owner section with veteran background

**Design decisions:**
- Built for elderly and non-tech-savvy users: large text (min 20px), high contrast, no carousels or confusing animations
- Phone number is #1 CTA — all other actions are secondary
- Large tap targets (min 48x48px) — works on any phone
- WCAG AA contrast throughout

### Tech Stack

Plain HTML + CSS + Vanilla JS — zero dependencies, zero build step, opens in any browser offline. Hosted free on GitHub Pages with automatic deployment on every push to `master`.

```
hamptons-elite-powerwashing/
├── index.html       # Full single-page site
├── style.css        # Mobile-first responsive styles
├── script.js        # Mobile menu, smooth scroll, sticky header
├── README.md        # This file
├── BUSINESS-PLAN.txt
└── images/
    ├── before-1.jpg  # Driveway (replace with real photos)
    ├── after-1.jpg
    ├── before-2.jpg  # Siding
    ├── after-2.jpg
    ├── before-3.jpg  # Deck
    ├── after-3.jpg
    ├── before-4.jpg  # Commercial
    └── after-4.jpg
```

### Color Scheme

| Role | Color | Hex |
|------|-------|-----|
| Primary | Navy | `#0A2342` |
| Accent | Orange | `#FF6B00` |
| Highlight | Gold (veteran) | `#FFD700` |
| Background | White | `#FFFFFF` |
| Text | Near-black | `#1A1A1A` |
| Alt sections | Light gray | `#F5F5F5` |

### Pre-Launch Setup Checklist

1. Replace `(631) XXX-XXXX` with the real phone number — search for `XXX-XXXX` in `index.html`
2. Create a free account at [formspree.io](https://formspree.io) → new form → copy the Form ID → replace `YOUR_FORMSPREE_ID` in `index.html`
3. Drop real before/after photos into `images/` (same filenames)
4. Replace placeholder testimonials with real Google reviews as they come in
5. Create a [Google Business Profile](https://business.google.com) and paste the URL into the "Leave a Review" button href

**To go live:** Drag the folder to [netlify.com/drop](https://app.netlify.com/drop) — no account needed, live in 60 seconds. Or push to `master` — GitHub Pages auto-deploys within 2 minutes.

### Deploying an Update

```bash
cd "C:/Users/Sean Goudy/Desktop/hamptons-elite-powerwashing"
git add index.html style.css
git commit -m "describe what changed"
git push
```

### SEO Notes

- `<title>` and `<meta description>` target "pressure washing Long Island", "Nassau County", "Suffolk County"
- LocalBusiness JSON-LD schema in `<head>` — update phone/address when real info is confirmed
- Town name list in Service Area section drives geographic relevance in Google local results
- All image `alt` tags pre-filled — update when real photos are swapped in

---

## Phase 2 — AI-Powered Operations (Planned)

The website is Phase 1. Phase 2 transforms the business from a manually-operated service company into a **semi-automated operation** powered by AI agents — without losing the personal touch that wins repeat customers.

### Core Principle: Owner Always in Control

Every agent drafts, logs, and waits for approval. Nothing is ever sent automatically. The owner approves or edits every customer-facing action before it goes out. This keeps the business feeling personal and protects the reputation.

### The Six Agents

**1. Leads Agent**
When a customer submits the callback form, the Leads Agent drafts a personalized follow-up text or email within minutes. The owner gets a notification, reviews the draft, and approves it with one tap. First-response time goes from "whenever I see it" to under 5 minutes — without the owner writing anything from scratch.

**2. Scheduling Agent**
When a lead is qualified, the Scheduling Agent looks at the job calendar and drafts a time slot offer. The owner confirms the slot, then the customer is notified. Eliminates phone-tag and double-booking.

**3. Reviews Agent**
24 hours after a job is marked complete, the Reviews Agent drafts a personalized thank-you message with a Google review request. The owner approves, it sends. More reviews = higher search ranking = more inbound leads.

**4. Finance Agent**
After a job, the Finance Agent generates a professional invoice from the job record (customer, service, price, address). The owner reviews it, then it goes to the customer. Consistent formatting, no manual work.

**5. Marketing Agent**
After every job with a good before/after photo, the Marketing Agent drafts an Instagram or Facebook post with a caption. The owner approves before it publishes. Consistent social presence with minimal time investment.

**6. Estimating Agent**
Customer enters address and service type on the website — agent calculates a ballpark estimate based on property size, service, and location. Owner confirms before it's sent as a formal quote. Faster quotes close more jobs.

### Why the Website Is Already Agent-Ready

The callback form fields were built with agent parsing in mind — clean, consistent names: `name`, `phone`, `email`, `service`, `address`, `time`, `notes`. Formspree supports webhooks, so when Phase 2 is ready, form submissions pipe directly into the agent workflow with no changes to the website.

### Phase 2 Tech Stack (Planned)

- **Claude API** (claude-sonnet) — agent reasoning and message drafting
- **Formspree webhooks** — form submission trigger
- **Twilio** — SMS approval flow for the owner
- **SQLite or Airtable** — job and lead logging
- **Approval UI** — owner receives a notification with approve/edit/reject — one tap to send

---

## Phase 3 — Scale (Future Backlog)

Once Phase 2 is running smoothly:

- **Online self-booking** — customers pick a time slot on the website, owner confirms with one tap
- **Seasonal outreach** — spring/fall reminder drafts to past customers, owner approves each batch before sending
- **Referral tracking** — unique links per customer, agents track referrals and draft reward messages
- **Job photo archive** — field photos automatically attached to job records, continuously updating the before/after gallery
- **Multi-crew scheduling** — as the business scales to multiple crews, the Scheduling Agent handles routing and capacity

---

## Business Model Summary

| Phase | Status | What It Unlocks |
|-------|--------|----------------|
| Phase 1 — Website | Complete | Online presence, inbound leads, local SEO, credibility |
| Phase 2 — AI Agents | Planned | Faster response, consistent follow-up, less manual work per job |
| Phase 3 — Growth Tools | Future | Scale operations without proportional headcount increase |

---

*Phase 1 completed March 2026. Built with Claude Code.*
