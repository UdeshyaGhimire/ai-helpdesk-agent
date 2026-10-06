import sqlite3

DB_NAME = "helpdesk.db"


def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tickets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            message TEXT NOT NULL,
            category TEXT NOT NULL,
            priority TEXT NOT NULL,
            summary TEXT NOT NULL,
            answer TEXT NOT NULL,
            needs_human BOOLEAN NOT NULL,
            status TEXT NOT NULL DEFAULT 'Open'
        )
    """)

    conn.commit()
    conn.close()


def create_ticket(
    message,
    category,
    priority,
    summary,
    answer,
    needs_human,
    status="Open"
):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO tickets (
            message,
            category,
            priority,
            summary,
            answer,
            needs_human,
            status
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        message,
        category,
        priority,
        summary,
        answer,
        needs_human,
        status
    ))

    ticket_id = cursor.lastrowid

    conn.commit()
    conn.close()

    return ticket_id

def get_all_tickets():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            id,
            message,
            category,
            priority,
            summary,
            answer,
            needs_human,
            status
        FROM tickets
        ORDER BY id DESC
    """)

    rows = cursor.fetchall()
    conn.close()

    return [dict(row) for row in rows]


def get_ticket_by_id(ticket_id):
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            id,
            message,
            category,
            priority,
            summary,
            answer,
            needs_human,
            status
        FROM tickets
        WHERE id = ?
    """, (ticket_id,))

    row = cursor.fetchone()
    conn.close()

    if row is None:
        return None

    return dict(row)

def update_ticket_status(ticket_id, status):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE tickets
        SET status = ?
        WHERE id = ?
    """, (
        status,
        ticket_id
    ))

    updated_rows = cursor.rowcount

    conn.commit()
    conn.close()

    return updated_rows > 0