-- AI Business with Automated Agents — Database Schema

CREATE TABLE IF NOT EXISTS leads (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    phone TEXT,
    email TEXT,
    service TEXT,
    address TEXT,
    notes TEXT,
    call_time TEXT,
    status TEXT DEFAULT 'new',
    source TEXT DEFAULT 'formspree',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS jobs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    lead_id INTEGER REFERENCES leads(id),
    service TEXT NOT NULL,
    scheduled_date DATE,
    scheduled_time TEXT,
    duration_minutes INTEGER,
    price_agreed REAL,
    status TEXT DEFAULT 'scheduled',
    address TEXT,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP
);

CREATE TABLE IF NOT EXISTS drafts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    agent TEXT NOT NULL,
    lead_id INTEGER REFERENCES leads(id),
    job_id INTEGER REFERENCES jobs(id),
    draft_text TEXT NOT NULL,
    recipient_name TEXT,
    recipient_phone TEXT,
    recipient_email TEXT,
    status TEXT DEFAULT 'pending',
    approved_at TIMESTAMP,
    sent_at TIMESTAMP,
    owner_edits TEXT,
    metadata TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS invoices (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    job_id INTEGER REFERENCES jobs(id),
    invoice_number TEXT UNIQUE NOT NULL,
    line_items TEXT NOT NULL,
    subtotal REAL,
    tax REAL,
    total REAL,
    status TEXT DEFAULT 'draft',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS activity_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    agent TEXT,
    action TEXT NOT NULL,
    draft_id INTEGER REFERENCES drafts(id),
    details TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
