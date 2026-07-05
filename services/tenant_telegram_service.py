from database import get_connection
import logging

logger = logging.getLogger(__name__)


def connect_telegram_bot(
    tenant_slug: str,
    bot_username: str,
    bot_token: str = None,
):
    conn = get_connection()

    try:
        # Find tenant by slug
        tenant = conn.execute(
            """
            SELECT id
            FROM tenants
            WHERE slug = ?
            """,
            (tenant_slug,)
        ).fetchone()

        if tenant is None:
            raise ValueError(
                f"No tenant found with slug '{tenant_slug}'"
            )

        tenant_id = tenant["id"]

        # Check if bot already exists
        existing = conn.execute(
            """
            SELECT id
            FROM tenant_telegram_bots
            WHERE bot_username = ?
            """,
            (bot_username,)
        ).fetchone()

        if existing:
            conn.execute(
                """
                UPDATE tenant_telegram_bots
                SET
                    tenant_id = ?,
                    bot_token = ?,
                    active = 1
                WHERE bot_username = ?
                """,
                (
                    tenant_id,
                    bot_token,
                    bot_username,
                )
            )

            print(f"Updated Telegram bot '{bot_username}'.")

        else:
            conn.execute(
                """
                INSERT INTO tenant_telegram_bots(
                    tenant_id,
                    bot_username,
                    bot_token
                )
                VALUES (?, ?, ?)
                """,
                (
                    tenant_id,
                    bot_username,
                    bot_token,
                )
            )

            print(f"Registered Telegram bot '{bot_username}'.")

        conn.commit()

    finally:
        conn.close()


def get_tenant_by_bot_username(bot_username):

    logger.info(
        "Searching Telegram tenant for '%s'",
        bot_username,
    )

    conn = get_connection()

    try:
        tenant = conn.execute(
            """
            SELECT
                t.*,
                tg.bot_username,
                tg.bot_token

            FROM tenant_telegram_bots tg

            JOIN tenants t
              ON t.id = tg.tenant_id

            WHERE tg.bot_username = ?
              AND tg.active = 1
              AND t.status = 'active'
            """,
            (bot_username,),
        ).fetchone()

        if tenant:
            logger.info(
                "Tenant Found: %s (ID=%s)",
                tenant["company_name"],
                tenant["id"],
            )
        else:
            logger.error(
                "No tenant mapped to bot '%s'",
                bot_username,
            )

        return tenant

    finally:
        conn.close()