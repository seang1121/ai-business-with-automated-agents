"""Seed demo data — populates the database with realistic sample data."""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.config import load_config
from backend.database import init_db, get_db, insert_lead, insert_job, insert_draft, \
    insert_invoice, log_activity, update_lead_status


DEMO_LEADS = [
    {
        "name": "Mike DiNardo",
        "phone": "(555) 234-5678",
        "email": "mike.d@example.com",
        "service": "Driveway & Walkway Cleaning",
        "address": "142 Oak St, Huntington",
        "notes": "Double-wide driveway, some oil stains near the garage.",
        "call_time": "Morning (8am-12pm)",
    },
    {
        "name": "Susan Reynolds",
        "phone": "(555) 345-6789",
        "email": "susan.r@example.com",
        "service": "House & Vinyl Siding Wash",
        "address": "89 Maple Ave, Babylon",
        "notes": "Green mold on the north side. Two-story colonial.",
        "call_time": "Afternoon (12pm-5pm)",
    },
    {
        "name": "Tom Kowalski",
        "phone": "(555) 456-7890",
        "email": "tom.k@example.com",
        "service": "Commercial Exterior",
        "address": "456 Main St, Farmingdale",
        "notes": "Restaurant exterior + parking lot. Monthly contract possible.",
        "call_time": "Morning (8am-12pm)",
    },
    {
        "name": "Jennifer Park",
        "phone": "(555) 567-8901",
        "email": "jen.p@example.com",
        "service": "Deck & Patio Cleaning",
        "address": "23 Birch Lane, Smithtown",
        "notes": "Composite deck, about 400 sq ft. Getting ready for summer.",
        "call_time": "Evening (5pm-8pm)",
    },
    {
        "name": "Robert Garcia",
        "phone": "(555) 678-9012",
        "email": "rob.g@example.com",
        "service": "Roof Soft Washing",
        "address": "711 Cedar Rd, Massapequa",
        "notes": "Black streaks on the roof. Asphalt shingles.",
        "call_time": "Afternoon (12pm-5pm)",
    },
]


def seed():
    config = load_config()
    init_db()
    db = get_db()

    # Check if already seeded
    existing = db.execute("SELECT COUNT(*) FROM leads").fetchone()[0]
    if existing > 0:
        print(f"Database already has {existing} leads. Skipping seed.")
        print("Delete business.db to re-seed.")
        return

    biz = config.business
    print(f"\nSeeding demo data for: {biz.get('name', 'Your Business')}")
    print(f"Mode: {config.mode.upper()}\n")

    # Insert leads
    lead_ids = []
    for lead_data in DEMO_LEADS:
        lead_id = insert_lead(**lead_data)
        lead_ids.append(lead_id)
        print(f"  Lead #{lead_id}: {lead_data['name']} — {lead_data['service']}")

    # Update some lead statuses
    update_lead_status(lead_ids[0], "contacted")
    update_lead_status(lead_ids[1], "ready_to_book")
    update_lead_status(lead_ids[2], "booked")

    # Insert jobs
    job1_id = insert_job(
        lead_id=lead_ids[2], service="Commercial Exterior",
        scheduled_date="2026-03-25", scheduled_time="08:00",
        duration_minutes=180, price_agreed=850.00,
        address="456 Main St, Farmingdale",
    )
    job2_id = insert_job(
        lead_id=lead_ids[0], service="Driveway & Walkway Cleaning",
        scheduled_date="2026-03-26", scheduled_time="09:00",
        duration_minutes=90, price_agreed=200.00,
        address="142 Oak St, Huntington",
    )
    job3_id = insert_job(
        lead_id=lead_ids[1], service="House & Vinyl Siding Wash",
        scheduled_date="2026-03-20", scheduled_time="10:00",
        duration_minutes=120, price_agreed=375.00,
        address="89 Maple Ave, Babylon",
    )
    # Mark job3 as complete
    db.execute(
        "UPDATE jobs SET status = 'complete', completed_at = CURRENT_TIMESTAMP "
        "WHERE id = ?", (job3_id,)
    )
    db.commit()
    print(f"\n  Job #{job1_id}: Commercial Exterior — scheduled")
    print(f"  Job #{job2_id}: Driveway Cleaning — scheduled")
    print(f"  Job #{job3_id}: House Wash — completed")

    # Insert agent drafts (mix of pending, approved, rejected)
    owner = biz.get("owner_name", "Owner")

    draft1 = insert_draft(
        agent="leads", lead_id=lead_ids[3],
        draft_text=(
            f"Hi Jennifer, thank you for reaching out to {biz.get('name', 'us')}! "
            f"We'd love to help with your deck cleaning. {owner} will personally "
            f"follow up to discuss your project and provide a free estimate. "
            f"Looking forward to it!"
        ),
        recipient_name="Jennifer Park",
        recipient_phone="(555) 567-8901",
    )

    draft2 = insert_draft(
        agent="estimating", lead_id=lead_ids[4],
        draft_text=(
            f"Hi Robert, based on your roof soft washing request at 711 Cedar Rd, "
            f"here's our preliminary estimate:\n\n"
            f"Estimated range: $350 - $770\n\n"
            f"This is a ballpark based on typical jobs in your area. {owner} will "
            f"confirm the exact price after a quick look (free, no obligation)."
        ),
        recipient_name="Robert Garcia",
        recipient_phone="(555) 678-9012",
    )

    draft3 = insert_draft(
        agent="scheduling", lead_id=lead_ids[1],
        draft_text=(
            f"Hi Susan, great news! We have the following times available "
            f"for your house wash:\n\n"
            f"1. Monday, March 24 at 9:00 AM\n"
            f"2. Wednesday, March 26 at 2:00 PM\n"
            f"3. Friday, March 28 at 10:00 AM\n\n"
            f"Which works best? — {owner}"
        ),
        recipient_name="Susan Reynolds",
        recipient_phone="(555) 345-6789",
    )

    draft4 = insert_draft(
        agent="reviews", job_id=job3_id, lead_id=lead_ids[1],
        draft_text=(
            f"Hi Susan, thank you so much for choosing {biz.get('name', 'us')} "
            f"for your house wash! We hope the siding looks amazing. "
            f"If you have a moment, we'd truly appreciate a quick review.\n\n"
            f"{biz.get('google_review_link', 'https://g.page/review')}\n\n"
            f"Thank you again! — {owner}"
        ),
        recipient_name="Susan Reynolds",
        recipient_email="susan.r@example.com",
    )

    draft5 = insert_draft(
        agent="finance", job_id=job3_id, lead_id=lead_ids[1],
        draft_text=(
            f"INVOICE #INV-1001\n"
            f"From: {biz.get('name', 'Your Business')}\n"
            f"To: Susan Reynolds\n"
            f"Date: March 20, 2026\n\n"
            f"Service: House & Vinyl Siding Wash\n"
            f"Subtotal: $375.00\n"
            f"Tax (8.625%): $32.34\n"
            f"Total: $407.34\n\n"
            f"Payment: Cash, Venmo, Check, Credit Card"
        ),
        recipient_name="Susan Reynolds",
        recipient_email="susan.r@example.com",
    )

    draft6 = insert_draft(
        agent="marketing", job_id=job3_id,
        draft_text=(
            f"Another job well done! We just completed a house & vinyl siding wash "
            f"and the results speak for themselves. Swipe to see the before & after!\n\n"
            f"Serving Nassau & Suffolk County with pride.\n"
            f"Call {biz.get('phone', '(555) 000-0000')} for your free estimate.\n\n"
            f"#localbusiness #beforeandafter"
        ),
        recipient_name="",
    )

    # Approve some, reject one
    from backend.approval.approval_manager import approve, reject
    approve(draft4)  # Reviews draft — approved
    approve(draft5)  # Finance draft — approved
    reject(draft6)   # Marketing draft — rejected (owner wanted different caption)

    # Log activities
    log_activity("leads", "draft_created", draft1, "New lead: Jennifer Park")
    log_activity("estimating", "draft_created", draft2, "Estimate for Robert Garcia")
    log_activity("scheduling", "draft_created", draft3, "Scheduling for Susan Reynolds")
    log_activity("reviews", "approved", draft4, "Review request approved for Susan")
    log_activity("finance", "approved", draft5, "Invoice approved for Susan")
    log_activity("marketing", "rejected", draft6, "Owner wanted different caption")
    log_activity("system", "job_complete", None, "Job #3 marked complete (House Wash)")

    print(f"\n  Draft #{draft1}: Leads — pending")
    print(f"  Draft #{draft2}: Estimating — pending")
    print(f"  Draft #{draft3}: Scheduling — pending")
    print(f"  Draft #{draft4}: Reviews — approved")
    print(f"  Draft #{draft5}: Finance — approved")
    print(f"  Draft #{draft6}: Marketing — rejected")

    print(f"\nDemo seeded! Start the server: python backend/app.py")
    print(f"Dashboard: http://localhost:5000/dashboard/ (PIN: 123456)\n")


if __name__ == "__main__":
    seed()
