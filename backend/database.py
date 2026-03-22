"""SQLite singleton wrapper."""

import json
import sqlite3
from contextlib import contextmanager
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / "business.db"
SCHEMA_PATH = Path(__file__).parent / "schema.sql"

_connection: sqlite3.Connection | None = None


def get_db() -> sqlite3.Connection:
    """Get or create the singleton database connection."""
    global _connection
    if _connection is None:
        _connection = sqlite3.connect(str(DB_PATH), check_same_thread=False)
        _connection.row_factory = sqlite3.Row
        _connection.execute("PRAGMA journal_mode=WAL")
        _connection.execute("PRAGMA foreign_keys=ON")
    return _connection


def init_db() -> None:
    """Create tables from schema.sql if they don't exist."""
    db = get_db()
    with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
        db.executescript(f.read())
    db.commit()


def close_db() -> None:
    """Close the database connection."""
    global _connection
    if _connection:
        _connection.close()
        _connection = None


@contextmanager
def transaction():
    """Context manager for database transactions."""
    db = get_db()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise


# --- Query helpers ---

def insert_lead(name: str, phone: str, email: str, service: str,
                address: str, notes: str, call_time: str) -> int:
    db = get_db()
    cursor = db.execute(
        "INSERT INTO leads (name, phone, email, service, address, notes, call_time) "
        "VALUES (?, ?, ?, ?, ?, ?, ?)",
        (name, phone, email, service, address, notes, call_time),
    )
    db.commit()
    return cursor.lastrowid


def get_lead(lead_id: int) -> dict | None:
    row = get_db().execute("SELECT * FROM leads WHERE id = ?", (lead_id,)).fetchone()
    return dict(row) if row else None


def update_lead_status(lead_id: int, status: str) -> None:
    get_db().execute(
        "UPDATE leads SET status = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?",
        (status, lead_id),
    )
    get_db().commit()


def get_all_leads(status: str | None = None) -> list[dict]:
    db = get_db()
    if status:
        rows = db.execute(
            "SELECT * FROM leads WHERE status = ? ORDER BY created_at DESC", (status,)
        ).fetchall()
    else:
        rows = db.execute("SELECT * FROM leads ORDER BY created_at DESC").fetchall()
    return [dict(r) for r in rows]


def insert_job(lead_id: int, service: str, scheduled_date: str,
               scheduled_time: str, duration_minutes: int,
               price_agreed: float | None, address: str) -> int:
    db = get_db()
    cursor = db.execute(
        "INSERT INTO jobs (lead_id, service, scheduled_date, scheduled_time, "
        "duration_minutes, price_agreed, address) VALUES (?, ?, ?, ?, ?, ?, ?)",
        (lead_id, service, scheduled_date, scheduled_time, duration_minutes,
         price_agreed, address),
    )
    db.commit()
    return cursor.lastrowid


def get_job(job_id: int) -> dict | None:
    row = get_db().execute("SELECT * FROM jobs WHERE id = ?", (job_id,)).fetchone()
    return dict(row) if row else None


def get_jobs_on_date(date: str) -> list[dict]:
    rows = get_db().execute(
        "SELECT * FROM jobs WHERE scheduled_date = ? AND status != 'cancelled' "
        "ORDER BY scheduled_time",
        (date,),
    ).fetchall()
    return [dict(r) for r in rows]


def complete_job(job_id: int) -> None:
    get_db().execute(
        "UPDATE jobs SET status = 'complete', completed_at = CURRENT_TIMESTAMP "
        "WHERE id = ?",
        (job_id,),
    )
    get_db().commit()


def insert_draft(agent: str, draft_text: str, lead_id: int | None = None,
                 job_id: int | None = None, recipient_name: str = "",
                 recipient_phone: str = "", recipient_email: str = "",
                 metadata: dict | None = None) -> int:
    db = get_db()
    cursor = db.execute(
        "INSERT INTO drafts (agent, lead_id, job_id, draft_text, recipient_name, "
        "recipient_phone, recipient_email, metadata) "
        "VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
        (agent, lead_id, job_id, draft_text, recipient_name, recipient_phone,
         recipient_email, json.dumps(metadata or {})),
    )
    db.commit()
    return cursor.lastrowid


def get_draft(draft_id: int) -> dict | None:
    row = get_db().execute("SELECT * FROM drafts WHERE id = ?", (draft_id,)).fetchone()
    return dict(row) if row else None


def get_pending_drafts() -> list[dict]:
    rows = get_db().execute(
        "SELECT * FROM drafts WHERE status = 'pending' ORDER BY created_at DESC"
    ).fetchall()
    return [dict(r) for r in rows]


def get_all_drafts(limit: int = 50) -> list[dict]:
    rows = get_db().execute(
        "SELECT * FROM drafts ORDER BY created_at DESC LIMIT ?", (limit,)
    ).fetchall()
    return [dict(r) for r in rows]


def approve_draft(draft_id: int, edits: str | None = None) -> None:
    db = get_db()
    if edits:
        db.execute(
            "UPDATE drafts SET status = 'approved', approved_at = CURRENT_TIMESTAMP, "
            "owner_edits = ? WHERE id = ?",
            (edits, draft_id),
        )
    else:
        db.execute(
            "UPDATE drafts SET status = 'approved', approved_at = CURRENT_TIMESTAMP "
            "WHERE id = ?",
            (draft_id,),
        )
    db.commit()


def reject_draft(draft_id: int) -> None:
    get_db().execute(
        "UPDATE drafts SET status = 'rejected' WHERE id = ?", (draft_id,)
    )
    get_db().commit()


def insert_invoice(job_id: int, invoice_number: str, line_items: list,
                   subtotal: float, tax: float, total: float) -> int:
    db = get_db()
    cursor = db.execute(
        "INSERT INTO invoices (job_id, invoice_number, line_items, subtotal, tax, total) "
        "VALUES (?, ?, ?, ?, ?, ?)",
        (job_id, invoice_number, json.dumps(line_items), subtotal, tax, total),
    )
    db.commit()
    return cursor.lastrowid


def log_activity(agent: str, action: str, draft_id: int | None = None,
                 details: str = "") -> None:
    get_db().execute(
        "INSERT INTO activity_log (agent, action, draft_id, details) "
        "VALUES (?, ?, ?, ?)",
        (agent, action, draft_id, details),
    )
    get_db().commit()


def get_activity_log(limit: int = 50) -> list[dict]:
    rows = get_db().execute(
        "SELECT * FROM activity_log ORDER BY created_at DESC LIMIT ?", (limit,)
    ).fetchall()
    return [dict(r) for r in rows]


def get_stats() -> dict:
    """Dashboard stats."""
    db = get_db()
    return {
        "total_leads": db.execute("SELECT COUNT(*) FROM leads").fetchone()[0],
        "new_leads": db.execute(
            "SELECT COUNT(*) FROM leads WHERE status = 'new'"
        ).fetchone()[0],
        "pending_drafts": db.execute(
            "SELECT COUNT(*) FROM drafts WHERE status = 'pending'"
        ).fetchone()[0],
        "approved_drafts": db.execute(
            "SELECT COUNT(*) FROM drafts WHERE status = 'approved'"
        ).fetchone()[0],
        "active_jobs": db.execute(
            "SELECT COUNT(*) FROM jobs WHERE status IN ('scheduled', 'in_progress')"
        ).fetchone()[0],
        "completed_jobs": db.execute(
            "SELECT COUNT(*) FROM jobs WHERE status = 'complete'"
        ).fetchone()[0],
    }
