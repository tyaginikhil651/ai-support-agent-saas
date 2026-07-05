import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logger = logging.getLogger(__name__)

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

import os

from dotenv import load_dotenv

from config import TELEGRAM_TOKEN

from graph.workflow import run_graph

from tools.customer import save_customer

from services.tenant_telegram_service import (
    get_tenant_by_bot_username,
)

from services.tenant_telegram_service import connect_telegram_bot

load_dotenv()

connect_telegram_bot(
    tenant_slug="abc-internet",
    bot_username="NIKHIL_958_AI_AGENT_bot",
    bot_token=os.getenv("TELEGRAM_TOKEN")
)


# ---------------------------------------
# START
# ---------------------------------------

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    try:
        user = update.effective_user

        logger.info("START received from user %s", user.id)

        bot = await context.bot.get_me()

        logger.info("Bot username: %s", bot.username)

        tenant = get_tenant_by_bot_username(bot.username)

        if tenant is None:
            logger.error("Unknown tenant for bot %s", bot.username)

            await update.message.reply_text(
                "Unknown tenant."
            )
            return

        save_customer(
            tenant_id=tenant["id"],
            platform_user_id=str(user.id),
            username=user.username or user.first_name,
            phone=""
        )

        logger.info("Customer saved successfully")

        await update.message.reply_text(
            f"Welcome to {tenant['company_name']}"
        )

    except Exception:
        logger.exception("Error in /start command")

        await update.message.reply_text(
            "Internal server error."
        )


# ---------------------------------------
# CHAT
# ---------------------------------------

async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):

    try:

        user = update.effective_user

        message = update.message.text

        logger.info("=" * 60)
        logger.info("Incoming Telegram Message")
        logger.info("User ID: %s", user.id)
        logger.info("Username: %s", user.username)
        logger.info("Message: %s", message)

        bot = await context.bot.get_me()

        logger.info("Bot Username: %s", bot.username)

        tenant = get_tenant_by_bot_username(bot.username)

        if tenant is None:

            logger.error("Unknown tenant")

            await update.message.reply_text(
                "Unknown tenant."
            )

            return

        logger.info("Tenant Found")
        logger.info("Tenant ID: %s", tenant["id"])
        logger.info("Company: %s", tenant["company_name"])

        save_customer(
            tenant_id=tenant["id"],
            platform_user_id=str(user.id),
            username=user.username or user.first_name,
            phone=""
        )

        logger.info("Customer saved")

        reply = run_graph(
            user_id=str(user.id),
            tenant_id=tenant["id"],
            message=message
        )

        logger.info("Graph Response:")
        logger.info(reply)

        await update.message.reply_text(reply)

        logger.info("Reply sent successfully")

    except Exception:
        logger.exception("Telegram Chat Error")

        await update.message.reply_text(
            "Something went wrong."
        )


async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):

    logger.exception(
        "Unhandled exception",
        exc_info=context.error
    )

# ---------------------------------------
# MAIN
# ---------------------------------------

def main():

    app = (
        Application.builder()
        .token(TELEGRAM_TOKEN)
        .build()
    )

    app.add_handler(
        CommandHandler(
            "start",
            start,
        )
    )

    app.add_handler(
        MessageHandler(
            filters.TEXT
            & ~filters.COMMAND,
            chat,
        )
    )

    app.add_error_handler(error_handler)

    print(
        "Telegram AI Agent Started..."
    )

    app.run_polling()


if __name__ == "__main__":
    main()


