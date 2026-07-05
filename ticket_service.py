import sqlite3
from datetime import datetime

DB_NAME = "support.db"


def create_ticket(user_id, issue):

    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    ticket_id = f"CMP-{int(datetime.now().timestamp())}"

    cur.execute("""
        INSERT INTO tickets
        (ticket_id,user_id,issue,status)
        VALUES (?,?,?,?)
    """, (
        ticket_id,
        user_id,
        issue,
        "OPEN"
    ))

    conn.commit()
    conn.close()

    return ticket_id


def get_ticket(ticket_id):

    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("""
        SELECT ticket_id,issue,status,created_at
        FROM tickets
        WHERE ticket_id=?
    """, (ticket_id,))

    row = cur.fetchone()

    conn.close()

    return row


def update_ticket(ticket_id, status):

    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("""
        UPDATE tickets
        SET status=?
        WHERE ticket_id=?
    """, (status, ticket_id))

    conn.commit()
    conn.close()


if __name__ == "__main__":
    create_ticket(
        user_id="user_123",
        issue="AC not cooling"
    )

    t = get_ticket("CMP-1687465920")
    print(t)

    update_ticket("CMP-1687465920", "CLOSED")