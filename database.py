import sqlite3
from datetime import datetime
import hashlib

DB_NAME = "insurance.db"


# ---------------------------------------------------------
# DATABASE CONNECTION
# ---------------------------------------------------------

def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


# ---------------------------------------------------------
# PASSWORD HASHING
# ---------------------------------------------------------

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


# ---------------------------------------------------------
# INITIALIZE DATABASE
# ---------------------------------------------------------

def init_db():

    conn = get_connection()
    cursor = conn.cursor()

    # USERS TABLE
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            full_name TEXT NOT NULL,
            role TEXT NOT NULL,
            email TEXT,
            created_at TEXT
        )
    """)

    # CUSTOMERS TABLE
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS customers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT,
            phone TEXT,
            address TEXT,
            dob TEXT,
            gender TEXT,
            created_at TEXT
        )
    """)

    # POLICIES TABLE
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS policies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            policy_number TEXT UNIQUE NOT NULL,
            customer_id INTEGER,
            policy_name TEXT NOT NULL,
            category TEXT NOT NULL,
            premium REAL DEFAULT 0,
            coverage_amount REAL DEFAULT 0,
            start_date TEXT,
            end_date TEXT,
            status TEXT DEFAULT 'Active',
            FOREIGN KEY(customer_id) REFERENCES customers(id)
        )
    """)

    # AGENTS TABLE
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS agents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT,
            phone TEXT,
            specialization TEXT,
            commission REAL DEFAULT 0,
            status TEXT DEFAULT 'Active',
            created_at TEXT
        )
    """)

    # CLAIMS TABLE
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS claims (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            claim_number TEXT UNIQUE NOT NULL,
            customer_id INTEGER,
            policy_id INTEGER,
            claim_amount REAL DEFAULT 0,
            claim_date TEXT,
            description TEXT,
            status TEXT DEFAULT 'Pending',
            FOREIGN KEY(customer_id) REFERENCES customers(id),
            FOREIGN KEY(policy_id) REFERENCES policies(id)
        )
    """)

    # PAYMENTS TABLE
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS payments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            payment_number TEXT UNIQUE NOT NULL,
            customer_id INTEGER,
            policy_id INTEGER,
            amount REAL DEFAULT 0,
            payment_date TEXT,
            payment_method TEXT,
            status TEXT DEFAULT 'Paid',
            FOREIGN KEY(customer_id) REFERENCES customers(id),
            FOREIGN KEY(policy_id) REFERENCES policies(id)
        )
    """)

    # DEFAULT ADMIN
    cursor.execute(
        "SELECT * FROM users WHERE username = ?",
        ("admin",)
    )

    if cursor.fetchone() is None:

        cursor.execute("""
            INSERT INTO users
            (username, password, full_name, role, email, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            "admin",
            hash_password("admin123"),
            "System Administrator",
            "Admin",
            "admin@insurance.com",
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ))

    conn.commit()
    conn.close()


# ---------------------------------------------------------
# LOGIN
# ---------------------------------------------------------

def authenticate_user(username, password):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM users
        WHERE username = ? AND password = ?
    """, (
        username,
        hash_password(password)
    ))

    user = cursor.fetchone()

    conn.close()

    if user:
        return dict(user)

    return None


# ---------------------------------------------------------
# USERS
# ---------------------------------------------------------

def add_user(username, password, full_name, role, email):

    conn = get_connection()
    cursor = conn.cursor()

    try:

        cursor.execute("""
            INSERT INTO users
            (username, password, full_name, role, email, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            username,
            hash_password(password),
            full_name,
            role,
            email,
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ))

        conn.commit()
        return True

    except sqlite3.IntegrityError:
        return False

    finally:
        conn.close()


# ---------------------------------------------------------
# CUSTOMERS
# ---------------------------------------------------------

def add_customer(name, email, phone, address, dob, gender):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO customers
        (name, email, phone, address, dob, gender, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        name,
        email,
        phone,
        address,
        dob,
        gender,
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ))

    conn.commit()
    conn.close()


def get_customers():

    conn = get_connection()

    data = conn.execute("""
        SELECT * FROM customers
        ORDER BY id DESC
    """).fetchall()

    conn.close()

    return [dict(row) for row in data]


def delete_customer(customer_id):

    conn = get_connection()

    conn.execute(
        "DELETE FROM customers WHERE id = ?",
        (customer_id,)
    )

    conn.commit()
    conn.close()


# ---------------------------------------------------------
# POLICIES
# ---------------------------------------------------------

def add_policy(
    policy_number,
    customer_id,
    policy_name,
    category,
    premium,
    coverage_amount,
    start_date,
    end_date,
    status
):

    conn = get_connection()

    try:

        conn.execute("""
            INSERT INTO policies
            (
                policy_number,
                customer_id,
                policy_name,
                category,
                premium,
                coverage_amount,
                start_date,
                end_date,
                status
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            policy_number,
            customer_id,
            policy_name,
            category,
            premium,
            coverage_amount,
            start_date,
            end_date,
            status
        ))

        conn.commit()
        return True

    except sqlite3.IntegrityError:
        return False

    finally:
        conn.close()


def get_policies():

    conn = get_connection()

    data = conn.execute("""
        SELECT
            policies.*,
            customers.name AS customer_name
        FROM policies
        LEFT JOIN customers
        ON policies.customer_id = customers.id
        ORDER BY policies.id DESC
    """).fetchall()

    conn.close()

    return [dict(row) for row in data]


# ---------------------------------------------------------
# AGENTS
# ---------------------------------------------------------

def add_agent(
    name,
    email,
    phone,
    specialization,
    commission,
    status
):

    conn = get_connection()

    conn.execute("""
        INSERT INTO agents
        (
            name,
            email,
            phone,
            specialization,
            commission,
            status,
            created_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        name,
        email,
        phone,
        specialization,
        commission,
        status,
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ))

    conn.commit()
    conn.close()


def get_agents():

    conn = get_connection()

    data = conn.execute("""
        SELECT * FROM agents
        ORDER BY id DESC
    """).fetchall()

    conn.close()

    return [dict(row) for row in data]


# ---------------------------------------------------------
# CLAIMS
# ---------------------------------------------------------

def add_claim(
    claim_number,
    customer_id,
    policy_id,
    claim_amount,
    claim_date,
    description
):

    conn = get_connection()

    try:

        conn.execute("""
            INSERT INTO claims
            (
                claim_number,
                customer_id,
                policy_id,
                claim_amount,
                claim_date,
                description,
                status
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            claim_number,
            customer_id,
            policy_id,
            claim_amount,
            claim_date,
            description,
            "Pending"
        ))

        conn.commit()
        return True

    except sqlite3.IntegrityError:
        return False

    finally:
        conn.close()


def get_claims():

    conn = get_connection()

    data = conn.execute("""
        SELECT
            claims.*,
            customers.name AS customer_name,
            policies.policy_number
        FROM claims
        LEFT JOIN customers
            ON claims.customer_id = customers.id
        LEFT JOIN policies
            ON claims.policy_id = policies.id
        ORDER BY claims.id DESC
    """).fetchall()

    conn.close()

    return [dict(row) for row in data]


def update_claim_status(claim_id, status):

    conn = get_connection()

    conn.execute("""
        UPDATE claims
        SET status = ?
        WHERE id = ?
    """, (
        status,
        claim_id
    ))

    conn.commit()
    conn.close()


# ---------------------------------------------------------
# PAYMENTS
# ---------------------------------------------------------

def add_payment(
    payment_number,
    customer_id,
    policy_id,
    amount,
    payment_date,
    payment_method
):

    conn = get_connection()

    try:

        conn.execute("""
            INSERT INTO payments
            (
                payment_number,
                customer_id,
                policy_id,
                amount,
                payment_date,
                payment_method,
                status
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            payment_number,
            customer_id,
            policy_id,
            amount,
            payment_date,
            payment_method,
            "Paid"
        ))

        conn.commit()
        return True

    except sqlite3.IntegrityError:
        return False

    finally:
        conn.close()


def get_payments():

    conn = get_connection()

    data = conn.execute("""
        SELECT
            payments.*,
            customers.name AS customer_name,
            policies.policy_number
        FROM payments
        LEFT JOIN customers
            ON payments.customer_id = customers.id
        LEFT JOIN policies
            ON payments.policy_id = policies.id
        ORDER BY payments.id DESC
    """).fetchall()

    conn.close()

    return [dict(row) for row in data]


# ---------------------------------------------------------
# DASHBOARD STATISTICS
# ---------------------------------------------------------

def get_dashboard_stats():

    conn = get_connection()

    customers = conn.execute(
        "SELECT COUNT(*) FROM customers"
    ).fetchone()[0]

    policies = conn.execute(
        "SELECT COUNT(*) FROM policies"
    ).fetchone()[0]

    claims = conn.execute(
        "SELECT COUNT(*) FROM claims"
    ).fetchone()[0]

    pending_claims = conn.execute("""
        SELECT COUNT(*)
        FROM claims
        WHERE status = 'Pending'
    """).fetchone()[0]

    agents = conn.execute(
        "SELECT COUNT(*) FROM agents"
    ).fetchone()[0]

    revenue = conn.execute("""
        SELECT COALESCE(SUM(amount), 0)
        FROM payments
        WHERE status = 'Paid'
    """).fetchone()[0]

    conn.close()

    return {
        "customers": customers,
        "policies": policies,
        "claims": claims,
        "pending_claims": pending_claims,
        "agents": agents,
        "revenue": revenue
    }


# ---------------------------------------------------------
# POLICY CATEGORY REPORT
# ---------------------------------------------------------

def get_policy_categories():

    conn = get_connection()

    data = conn.execute("""
        SELECT category, COUNT(*) AS total
        FROM policies
        GROUP BY category
    """).fetchall()

    conn.close()

    return [dict(row) for row in data]


# ---------------------------------------------------------
# CLAIM STATUS REPORT
# ---------------------------------------------------------

def get_claim_status():

    conn = get_connection()

    data = conn.execute("""
        SELECT status, COUNT(*) AS total
        FROM claims
        GROUP BY status
    """).fetchall()

    conn.close()

    return [dict(row) for row in data]