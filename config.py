# config.py

# Telegram Bot Token
TELEGRAM_TOKEN = "PASTE_YOUR_BOT_TOKEN_HERE"

# Ollama URL
OLLAMA_URL = "http://localhost:11434/api/generate"

# Ollama Model
MODEL_NAME = "llama3.2"

# Memory Files
USERS_FILE = "data/users.json"
APPOINTMENTS_FILE = "data/appointments.json"
COMPLAINTS_FILE = "data/complaints.json"
APP_SECRET_KEY = "MY_KEY"

##########################################################################################################


import os
from dotenv import load_dotenv


load_dotenv()


def get_env(
    name: str,
    default: str | None = None,
    required: bool = False
) -> str | None:
    value = os.getenv(name, default)

    if required and not value:
        raise RuntimeError(
            f"Missing required environment variable: {name}"
        )

    return value


APP_ENV = get_env(
    "APP_ENV",
    "development"
)

DEBUG = get_env(
    "DEBUG",
    "false"
).lower() == "true"

APP_SECRET_KEY = get_env(
    "APP_SECRET_KEY",
    required=True
)

DATABASE_URL = get_env(
    "DATABASE_URL",
    required=True
)

REDIS_URL = get_env(
    "REDIS_URL",
    required=True
)

JWT_SECRET_KEY = get_env(
    "JWT_SECRET_KEY",
    required=True
)

JWT_ALGORITHM = get_env(
    "JWT_ALGORITHM",
    "HS256"
)

JWT_EXPIRE_HOURS = int(
    get_env(
        "JWT_EXPIRE_HOURS",
        "24"
    )
)

META_ACCESS_TOKEN = get_env(
    "META_ACCESS_TOKEN",
    required=True
)

TELEGRAM_TOKEN = get_env(
    "TELEGRAM_TOKEN",
    required=True
)

WHATSAPP_VERIFY_TOKEN = get_env(
    "WHATSAPP_VERIFY_TOKEN",
    required=True
)

META_GRAPH_API_VERSION = get_env(
    "META_GRAPH_API_VERSION",
    "v23.0"
)

LOG_LEVEL = get_env(
    "LOG_LEVEL",
    "INFO"
)


# Gemini API Key
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Recommended model
MODEL_NAME = "gemini-2.5-flash"

