"""SQLite database layer: sample policies and support tickets."""
import sqlite3
from datetime import datetime

DB_PATH = "support.db"

SAMPLE_POLICIES = [
    ("POL1001", "Aarav Sharma", "Health", 500000, "2027-03-31", "Active"),
    ("POL1002", "Priya Reddy", "Motor", 350000, "2026-12-15", "Active"),
    ("POL1003", "Rahul Verma", "Life", 2000000, "2026-09-30", "Expired"),
    ("POL1004", "Sneha Iyer", "Travel", 100000, "2027-01-10", "Active"),
]


def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with get_conn() as conn:
        conn.execute("""CREATE TABLE IF NOT EXISTS policies (
            policy_no TEXT PRIMARY KEY, holder TEXT, type TEXT,
            cover_amount INTEGER, expiry_date TEXT, status TEXT)""")
        conn.execute("""CREATE TABLE IF NOT EXISTS tickets (
            id INTEGER PRIMARY KEY AUTOINCREMENT, policy_no TEXT,
            name TEXT, email TEXT, category TEXT, description TEXT,
            status TEXT DEFAULT 'Open', created_at TEXT)""")
        if conn.execute("SELECT COUNT(*) FROM policies").fetchone()[0] == 0:
            conn.executemany("INSERT INTO policies VALUES (?,?,?,?,?,?)", SAMPLE_POLICIES)


def get_policy(policy_no):
    with get_conn() as conn:
        row = conn.execute("SELECT * FROM policies WHERE policy_no = ?",
                           (policy_no.strip().upper(),)).fetchone()
    return dict(row) if row else None


def create_ticket(policy_no, name, email, category, description):
    with get_conn() as conn:
        cur = conn.execute(
            "INSERT INTO tickets (policy_no, name, email, category, description, created_at) "
            "VALUES (?,?,?,?,?,?)",
            (policy_no.strip().upper(), name, email, category, description,
             datetime.now().strftime("%Y-%m-%d %H:%M")))
        return cur.lastrowid


def get_ticket(ticket_id):
    with get_conn() as conn:
        row = conn.execute("SELECT * FROM tickets WHERE id = ?", (ticket_id,)).fetchone()
    return dict(row) if row else None


def get_all_tickets():
    with get_conn() as conn:
        return [dict(r) for r in conn.execute("SELECT * FROM tickets ORDER BY id DESC")]


def update_ticket_status(ticket_id, status):
    with get_conn() as conn:
        conn.execute("UPDATE tickets SET status = ? WHERE id = ?", (status, ticket_id))
