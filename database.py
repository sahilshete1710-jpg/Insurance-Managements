import sqlite3.connect(...)
import mysql.connector
from mysql.connector import Error
from datetime import datetime
import hashlib


# =========================================================
# MYSQL CONFIGURATION
# =========================================================

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "root123",
    "database": "insurance_management"
}


# =========================================================
# DATABASE CONNECTION
# =========================================================

def get_connection():

    try:
        connection = mysql.connector.connect(
            host=DB_CONFIG["host"],
            user=DB_CONFIG["user"],
            password=DB_CONFIG["password"],
            database=DB_CONFIG["database"]
        )

        return connection

    except Error as e:

        print("MySQL Connection Error:", e)

        return None


# =========================================================
# PASSWORD HASHING
# =========================================================

def hash_password(password):

    return hashlib.sha256(
        password.encode()
    ).hexdigest()


# =========================================================
# INITIALIZE DATABASE
# =========================================================

def init_db():

    conn = get_connection()

    if conn is None:
        return

    cursor = conn.cursor()

    # -----------------------------------------------------
    # USERS
    # -----------------------------------------------------

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (

            id INT AUTO_INCREMENT PRIMARY KEY,

            username VARCHAR(100) UNIQUE NOT NULL,

            password VARCHAR(255) NOT NULL,

            full_name VARCHAR(150) NOT NULL,

            role VARCHAR(50) NOT NULL,

            email VARCHAR(150),

            created_at DATETIME

        )
    """)


    # -----------------------------------------------------
    # CUSTOMERS
    # -----------------------------------------------------

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS customers (

            id INT AUTO_INCREMENT PRIMARY KEY,

            name VARCHAR(150) NOT NULL,

            email VARCHAR(150),

            phone VARCHAR(30),

            address TEXT,

            dob DATE,

            gender VARCHAR(30),

            created_at DATETIME

        )
    """)


    # -----------------------------------------------------
    # POLICIES
    # -----------------------------------------------------

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS policies (

            id INT AUTO_INCREMENT PRIMARY KEY,

            policy_number VARCHAR(100) UNIQUE NOT NULL,

            customer_id INT,

            policy_name VARCHAR(150) NOT NULL,

            category VARCHAR(100) NOT NULL,

            premium DECIMAL(15,2) DEFAULT 0,

            coverage_amount DECIMAL(15,2) DEFAULT 0,

            start_date DATE,

            end_date DATE,

            status VARCHAR(50) DEFAULT 'Active',

            FOREIGN KEY (customer_id)
                REFERENCES customers(id)
                ON DELETE SET NULL

        )
    """)


    # -----------------------------------------------------
    # AGENTS
    # -----------------------------------------------------

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS agents (

            id INT AUTO_INCREMENT PRIMARY KEY,

            name VARCHAR(150) NOT NULL,

            email VARCHAR(150),

            phone VARCHAR(30),

            specialization VARCHAR(100),

            commission DECIMAL(10,2) DEFAULT 0,

            status VARCHAR(50) DEFAULT 'Active',

            created_at DATETIME

        )
    """)


    # -----------------------------------------------------
    # CLAIMS
    # -----------------------------------------------------

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS claims (

            id INT AUTO_INCREMENT PRIMARY KEY,

            claim_number VARCHAR(100) UNIQUE NOT NULL,

            customer_id INT,

            policy_id INT,

            claim_amount DECIMAL(15,2) DEFAULT 0,

            claim_date DATE,

            description TEXT,

            status VARCHAR(50) DEFAULT 'Pending',

            FOREIGN KEY (customer_id)
                REFERENCES customers(id)
                ON DELETE SET NULL,

            FOREIGN KEY (policy_id)
                REFERENCES policies(id)
                ON DELETE SET NULL

        )
    """)


    # -----------------------------------------------------
    # PAYMENTS
    # -----------------------------------------------------

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS payments (

            id INT AUTO_INCREMENT PRIMARY KEY,

            payment_number VARCHAR(100) UNIQUE NOT NULL,

            customer_id INT,

            policy_id INT,

            amount DECIMAL(15,2) DEFAULT 0,

            payment_date DATE,

            payment_method VARCHAR(50),

            status VARCHAR(50) DEFAULT 'Paid',

            FOREIGN KEY (customer_id)
                REFERENCES customers(id)
                ON DELETE SET NULL,

            FOREIGN KEY (policy_id)
                REFERENCES policies(id)
                ON DELETE SET NULL

        )
    """)


    # -----------------------------------------------------
    # DEFAULT ADMIN
    # -----------------------------------------------------

    cursor.execute("""
        SELECT id
        FROM users
        WHERE username = %s
    """, ("admin",))

    admin = cursor.fetchone()

    if admin is None:

        cursor.execute("""
            INSERT INTO users
            (
                username,
                password,
                full_name,
                role,
                email,
                created_at
            )

            VALUES (%s, %s, %s, %s, %s, %s)
        """, (
            "admin",
            hash_password("admin123"),
            "System Administrator",
            "Admin",
            "admin@insurance.com",
            datetime.now()
        ))


    conn.commit()

    cursor.close()
    conn.close()


# =========================================================
# LOGIN
# =========================================================

def authenticate_user(username, password):

    conn = get_connection()

    if conn is None:
        return None

    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT *
        FROM users

        WHERE username = %s
        AND password = %s
    """, (
        username,
        hash_password(password)
    ))

    user = cursor.fetchone()

    cursor.close()
    conn.close()

    return user


# =========================================================
# ADD USER
# =========================================================

def add_user(
    username,
    password,
    full_name,
    role,
    email
):

    conn = get_connection()

    if conn is None:
        return False

    cursor = conn.cursor()

    try:

        cursor.execute("""
            INSERT INTO users
            (
                username,
                password,
                full_name,
                role,
                email,
                created_at
            )

            VALUES (%s, %s, %s, %s, %s, %s)
        """, (
            username,
            hash_password(password),
            full_name,
            role,
            email,
            datetime.now()
        ))

        conn.commit()

        return True

    except Error:

        return False

    finally:

        cursor.close()
        conn.close()


# =========================================================
# CUSTOMERS
# =========================================================

def add_customer(
    name,
    email,
    phone,
    address,
    dob,
    gender
):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO customers
        (
            name,
            email,
            phone,
            address,
            dob,
            gender,
            created_at
        )

        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (
        name,
        email,
        phone,
        address,
        dob,
        gender,
        datetime.now()
    ))

    conn.commit()

    cursor.close()
    conn.close()


def get_customers():

    conn = get_connection()

    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT *
        FROM customers
        ORDER BY id DESC
    """)

    data = cursor.fetchall()

    cursor.close()
    conn.close()

    return data


def delete_customer(customer_id):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM customers
        WHERE id = %s
    """, (customer_id,))

    conn.commit()

    cursor.close()
    conn.close()


# =========================================================
# POLICIES
# =========================================================

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

    cursor = conn.cursor()

    try:

        cursor.execute("""
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

            VALUES
            (%s,%s,%s,%s,%s,%s,%s,%s,%s)
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

    except Error:

        return False

    finally:

        cursor.close()
        conn.close()


def get_policies():

    conn = get_connection()

    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT

            policies.*,

            customers.name AS customer_name

        FROM policies

        LEFT JOIN customers
        ON policies.customer_id = customers.id

        ORDER BY policies.id DESC
    """)

    data = cursor.fetchall()

    cursor.close()
    conn.close()

    return data


# =========================================================
# AGENTS
# =========================================================

def add_agent(
    name,
    email,
    phone,
    specialization,
    commission,
    status
):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
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

        VALUES
        (%s,%s,%s,%s,%s,%s,%s)
    """, (
        name,
        email,
        phone,
        specialization,
        commission,
        status,
        datetime.now()
    ))

    conn.commit()

    cursor.close()
    conn.close()


def get_agents():

    conn = get_connection()

    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT *
        FROM agents
        ORDER BY id DESC
    """)

    data = cursor.fetchall()

    cursor.close()
    conn.close()

    return data


# =========================================================
# CLAIMS
# =========================================================

def add_claim(
    claim_number,
    customer_id,
    policy_id,
    claim_amount,
    claim_date,
    description
):

    conn = get_connection()

    cursor = conn.cursor()

    try:

        cursor.execute("""
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

            VALUES
            (%s,%s,%s,%s,%s,%s,%s)
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

    except Error:

        return False

    finally:

        cursor.close()
        conn.close()


def get_claims():

    conn = get_connection()

    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
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
    """)

    data = cursor.fetchall()

    cursor.close()
    conn.close()

    return data


def update_claim_status(
    claim_id,
    status
):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
        UPDATE claims

        SET status = %s

        WHERE id = %s
    """, (
        status,
        claim_id
    ))

    conn.commit()

    cursor.close()
    conn.close()


# =========================================================
# PAYMENTS
# =========================================================

def add_payment(
    payment_number,
    customer_id,
    policy_id,
    amount,
    payment_date,
    payment_method
):

    conn = get_connection()

    cursor = conn.cursor()

    try:

        cursor.execute("""
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

            VALUES
            (%s,%s,%s,%s,%s,%s,%s)
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

    except Error:

        return False

    finally:

        cursor.close()
        conn.close()


def get_payments():

    conn = get_connection()

    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
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
    """)

    data = cursor.fetchall()

    cursor.close()
    conn.close()

    return data


# =========================================================
# DASHBOARD STATISTICS
# =========================================================

def get_dashboard_stats():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        "SELECT COUNT(*) FROM customers"
    )

    customers = cursor.fetchone()[0]


    cursor.execute(
        "SELECT COUNT(*) FROM policies"
    )

    policies = cursor.fetchone()[0]


    cursor.execute(
        "SELECT COUNT(*) FROM claims"
    )

    claims = cursor.fetchone()[0]


    cursor.execute("""
        SELECT COUNT(*)

        FROM claims

        WHERE status = 'Pending'
    """)

    pending_claims = cursor.fetchone()[0]


    cursor.execute(
        "SELECT COUNT(*) FROM agents"
    )

    agents = cursor.fetchone()[0]


    cursor.execute("""
        SELECT COALESCE(SUM(amount), 0)

        FROM payments

        WHERE status = 'Paid'
    """)

    revenue = cursor.fetchone()[0]


    cursor.close()
    conn.close()


    return {

        "customers": customers,

        "policies": policies,

        "claims": claims,

        "pending_claims": pending_claims,

        "agents": agents,

        "revenue": float(revenue)

    }


# =========================================================
# POLICY CATEGORY REPORT
# =========================================================

def get_policy_categories():

    conn = get_connection()

    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT

            category,

            COUNT(*) AS total

        FROM policies

        GROUP BY category
    """)

    data = cursor.fetchall()

    cursor.close()
    conn.close()

    return data


# =========================================================
# CLAIM STATUS REPORT
# =========================================================

def get_claim_status():

    conn = get_connection()

    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT

            status,

            COUNT(*) AS total

        FROM claims

        GROUP BY status
    """)

    data = cursor.fetchall()

    cursor.close()
    conn.close()

    return data