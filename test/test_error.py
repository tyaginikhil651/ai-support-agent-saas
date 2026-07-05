from database import get_connection

conn = get_connection()

conn.execute("""
UPDATE tenant_telegram_bots
SET tenant_id = ?
WHERE bot_username = ?
""", (
    1,
    "NIKHIL_958_AI_AGENT_bot"
))

conn.commit()
conn.close()

print("Updated successfully.")