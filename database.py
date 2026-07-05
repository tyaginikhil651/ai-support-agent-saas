import sqlite3

DB_NAME = "support.db"


def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_connection()
    cur = conn.cursor()

    # ----------------------------------
    # TENANTS / COMPANIES
    # ----------------------------------
    cur.execute("""
    CREATE TABLE IF NOT EXISTS tenants(
        id INTEGER PRIMARY KEY AUTOINCREMENT,

        company_name TEXT NOT NULL,
        slug TEXT UNIQUE NOT NULL,

        email TEXT,
        phone TEXT,

        whatsapp_phone_number_id TEXT UNIQUE,
        whatsapp_business_account_id TEXT,

        plan TEXT DEFAULT 'starter',
        status TEXT DEFAULT 'active',

        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # ----------------------------------
    # ADMIN USERS: owner / manager / agent
    # ----------------------------------
    cur.execute("""
    CREATE TABLE IF NOT EXISTS admins(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        tenant_id INTEGER NOT NULL,
        username TEXT NOT NULL,
        email TEXT NOT NULL,
        password TEXT NOT NULL,
        role TEXT NOT NULL DEFAULT 'owner',
        active INTEGER DEFAULT 1,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

        UNIQUE(tenant_id, username),
        UNIQUE(tenant_id, email),

        FOREIGN KEY (tenant_id) REFERENCES tenants(id)
    )
    """)

    # ----------------------------------
    # CUSTOMERS
    # platform_user_id can be WhatsApp number,
    # Telegram ID, website-chat ID, etc.
    # ----------------------------------
    cur.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        tenant_id INTEGER NOT NULL,
        platform_user_id TEXT NOT NULL,
        username TEXT,
        phone TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

        UNIQUE(tenant_id, platform_user_id),

        FOREIGN KEY (tenant_id) REFERENCES tenants(id)
    )
    """)

    # ----------------------------------
    # TICKETS
    # ----------------------------------
    cur.execute("""
    CREATE TABLE IF NOT EXISTS tickets(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        tenant_id INTEGER NOT NULL,
        ticket_id TEXT NOT NULL,
        user_id TEXT NOT NULL,
        issue TEXT NOT NULL,
        status TEXT DEFAULT 'Open',
        priority TEXT DEFAULT 'Medium',
        assigned_to TEXT,
        escalated INTEGER DEFAULT 0,
        estimated_resolution TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

        UNIQUE(tenant_id, ticket_id),

        FOREIGN KEY (tenant_id) REFERENCES tenants(id)
    )
    """)

    # ----------------------------------
    # APPOINTMENTS
    # ----------------------------------
    cur.execute("""
    CREATE TABLE IF NOT EXISTS appointments(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        tenant_id INTEGER NOT NULL,
        user_id TEXT NOT NULL,
        service TEXT NOT NULL,
        date TEXT NOT NULL,
        calendar_link TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

        FOREIGN KEY (tenant_id) REFERENCES tenants(id)
    )
    """)

    # ----------------------------------
    # MULTI-TURN CONVERSATION STATE
    # ----------------------------------
    cur.execute("""
    CREATE TABLE IF NOT EXISTS sessions(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        tenant_id INTEGER NOT NULL,
        user_id TEXT NOT NULL,
        flow TEXT,
        step TEXT,
        data TEXT,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

        UNIQUE(tenant_id, user_id),

        FOREIGN KEY (tenant_id) REFERENCES tenants(id)
    )
    """)

    # ----------------------------------
    # TICKET REPLIES
    # ----------------------------------
    cur.execute("""
    CREATE TABLE IF NOT EXISTS replies(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        tenant_id INTEGER NOT NULL,
        ticket_id TEXT NOT NULL,
        message TEXT NOT NULL,
        sender TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

        FOREIGN KEY (tenant_id) REFERENCES tenants(id)
    )
    """)

    # ----------------------------------
    # CUSTOMER PROFILE / AI MEMORY
    # ----------------------------------
    cur.execute("""
    CREATE TABLE IF NOT EXISTS customer_profile(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        tenant_id INTEGER NOT NULL,
        user_id TEXT NOT NULL,
        total_messages INTEGER DEFAULT 0,
        complaint_count INTEGER DEFAULT 0,
        appointment_count INTEGER DEFAULT 0,
        sentiment_score REAL DEFAULT 0,
        last_intent TEXT,
        last_active TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        vip_score REAL DEFAULT 0,

        UNIQUE(tenant_id, user_id),

        FOREIGN KEY (tenant_id) REFERENCES tenants(id)
    )
    """)

    # ----------------------------------
    # SUPPORT AGENTS
    # ----------------------------------
    cur.execute("""
    CREATE TABLE IF NOT EXISTS agents(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        tenant_id INTEGER NOT NULL,
        name TEXT NOT NULL,
        email TEXT,
        skill TEXT,
        active_tickets INTEGER DEFAULT 0,
        status TEXT DEFAULT 'online',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

        FOREIGN KEY (tenant_id) REFERENCES tenants(id)
    )
    """)

    # Helpful indexes
    cur.execute("""
    CREATE INDEX IF NOT EXISTS idx_tickets_tenant_id
    ON tickets(tenant_id)
    """)

    cur.execute("""
    CREATE INDEX IF NOT EXISTS idx_users_tenant_id
    ON users(tenant_id)
    """)

    cur.execute("""
    CREATE INDEX IF NOT EXISTS idx_appointments_tenant_id
    ON appointments(tenant_id)
    """)
    
    # ----------------------------------
    # WHATSAPP TENANT CONFIGURATION
    # ----------------------------------

    cur.execute("""
    CREATE TABLE IF NOT EXISTS tenant_whatsapp_numbers(
        id INTEGER PRIMARY KEY AUTOINCREMENT,

        tenant_id INTEGER NOT NULL,

        phone_number_id TEXT UNIQUE NOT NULL,

        display_phone_number TEXT,

        verify_token TEXT,

        active INTEGER DEFAULT 1,

        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

        FOREIGN KEY (tenant_id) REFERENCES tenants(id)
    )
    """)


    cur.execute("""
    CREATE TABLE IF NOT EXISTS tenant_telegram_bots (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        tenant_id INTEGER NOT NULL,

        bot_username TEXT NOT NULL UNIQUE,

        bot_token TEXT,

        active INTEGER DEFAULT 1,

        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

        FOREIGN KEY (tenant_id)
            REFERENCES tenants(id)
    )
    """)

    conn.commit()
    conn.close()

    print("Database initialized successfully")


if __name__ == "__main__":
    init_db()


    