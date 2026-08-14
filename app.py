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
    "password": "YOUR_MYSQL_PASSWORD",
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
        password.encode("utf-8")
    ).hexdigest()


# =========================================================
# INITIALIZE DATABASE
# =========================================================

def init_db():

    connection = get_connection()

    if connection is None:
        return False

    cursor = connection.cursor()

    try:

        # -------------------------------------------------
        # USERS
        # -------------------------------------------------

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

        # -------------------------------------------------
        # CUSTOMERS
        # -------------------------------------------------

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

        # -------------------------------------------------
        # POLICIES
        # -------------------------------------------------

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

        # -------------------------------------------------
        # AGENTS
        # -------------------------------------------------

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

        # -------------------------------------------------
        # CLAIMS
        # -------------------------------------------------

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

        # -------------------------------------------------
        # PAYMENTS
        # -------------------------------------------------

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

        # -------------------------------------------------
        # DEFAULT ADMIN
        # -------------------------------------------------

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

        connection.commit()

        return True

    except Error as e:

        print("Database Initialization Error:", e)

        return False

    finally:

        cursor.close()
        connection.close()


# =========================================================
# LOGIN
# =========================================================

def authenticate_user(username, password):

    connection = get_connection()

    if connection is None:
        return None

    cursor = connection.cursor(dictionary=True)

    try:

        cursor.execute("""
            SELECT *
            FROM users
            WHERE username = %s
            AND password = %s
        """, (
            username,
            hash_password(password)
        ))

        return cursor.fetchone()

    except Error as e:

        print("Login Error:", e)

        return None

    finally:

        cursor.close()
        connection.close()


# =========================================================
# USER MANAGEMENT
# =========================================================

def add_user(
    username,
    password,
    full_name,
    role,
    email
):

    connection = get_connection()

    if connection is None:
        return False

    cursor = connection.cursor()

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

        connection.commit()

        return True

    except Error as e:

        print("Add User Error:", e)

        return False

    finally:

        cursor.close()
        connection.close()


def get_users():

    connection = get_connection()

    if connection is None:
        return []

    cursor = connection.cursor(dictionary=True)

    try:

        cursor.execute("""
            SELECT
                id,
                username,
                full_name,
                role,
                email,
                created_at
            FROM users
            ORDER BY id DESC
        """)

        return cursor.fetchall()

    except Error as e:

        print("Get Users Error:", e)

        return []

    finally:

        cursor.close()
        connection.close()


# =========================================================
# CUSTOMER MANAGEMENT
# =========================================================

def add_customer(
    name,
    email,
    phone,
    address,
    dob,
    gender
):

    connection = get_connection()

    if connection is None:
        return False

    cursor = connection.cursor()

    try:

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

        connection.commit()

        return True

    except Error as e:

        print("Add Customer Error:", e)

        return False

    finally:

        cursor.close()
        connection.close()


def get_customers():

    connection = get_connection()

    if connection is None:
        return []

    cursor = connection.cursor(dictionary=True)

    try:

        cursor.execute("""
            SELECT *
            FROM customers
            ORDER BY id DESC
        """)

        return cursor.fetchall()

    except Error as e:

        print("Get Customers Error:", e)

        return []

    finally:

        cursor.close()
        connection.close()


def update_customer(
    customer_id,
    name,
    email,
    phone,
    address,
    dob,
    gender
):

    connection = get_connection()

    if connection is None:
        return False

    cursor = connection.cursor()

    try:

        cursor.execute("""
            UPDATE customers
            SET
                name = %s,
                email = %s,
                phone = %s,
                address = %s,
                dob = %s,
                gender = %s
            WHERE id = %s
        """, (
            name,
            email,
            phone,
            address,
            dob,
            gender,
            customer_id
        ))

        connection.commit()

        return True

    except Error as e:

        print("Update Customer Error:", e)

        return False

    finally:

        cursor.close()
        connection.close()


def delete_customer(customer_id):

    connection = get_connection()

    if connection is None:
        return False

    cursor = connection.cursor()

    try:

        cursor.execute("""
            DELETE FROM customers
            WHERE id = %s
        """, (customer_id,))

        connection.commit()

        return True

    except Error as e:

        print("Delete Customer Error:", e)

        return False

    finally:

        cursor.close()
        connection.close()


# =========================================================
# POLICY MANAGEMENT
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

    connection = get_connection()

    if connection is None:
        return False

    cursor = connection.cursor()

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
            (%s, %s, %s, %s, %s, %s, %s, %s, %s)
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

        connection.commit()

        return True

    except Error as e:

        print("Add Policy Error:", e)

        return False

    finally:

        cursor.close()
        connection.close()


def get_policies():

    connection = get_connection()

    if connection is None:
        return []

    cursor = connection.cursor(dictionary=True)

    try:

        cursor.execute("""
            SELECT
                policies.*,
                customers.name AS customer_name

            FROM policies

            LEFT JOIN customers
                ON policies.customer_id = customers.id

            ORDER BY policies.id DESC
        """)

        return cursor.fetchall()

    except Error as e:

        print("Get Policies Error:", e)

        return []

    finally:

        cursor.close()
        connection.close()


def update_policy_status(
    policy_id,
    status
):

    connection = get_connection()

    if connection is None:
        return False

    cursor = connection.cursor()

    try:

        cursor.execute("""
            UPDATE policies
            SET status = %s
            WHERE id = %s
        """, (
            status,
            policy_id
        ))

        connection.commit()

        return True

    except Error as e:

        print("Update Policy Error:", e)

        return False

    finally:

        cursor.close()
        connection.close()


# =========================================================
# AGENT MANAGEMENT
# =========================================================

def add_agent(
    name,
    email,
    phone,
    specialization,
    commission,
    status
):

    connection = get_connection()

    if connection is None:
        return False

    cursor = connection.cursor()

    try:

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
            (%s, %s, %s, %s, %s, %s, %s)
        """, (
            name,
            email,
            phone,
            specialization,
            commission,
            status,
            datetime.now()
        ))

        connection.commit()

        return True

    except Error as e:

        print("Add Agent Error:", e)

        return False

    finally:

        cursor.close()
        connection.close()


def get_agents():

    connection = get_connection()

    if connection is None:
        return []

    cursor = connection.cursor(dictionary=True)

    try:

        cursor.execute("""
            SELECT *
            FROM agents
            ORDER BY id DESC
        """)

        return cursor.fetchall()

    except Error as e:

        print("Get Agents Error:", e)

        return []

    finally:

        cursor.close()
        connection.close()


# =========================================================
# CLAIM MANAGEMENT
# =========================================================

def add_claim(
    claim_number,
    customer_id,
    policy_id,
    claim_amount,
    claim_date,
    description
):

    connection = get_connection()

    if connection is None:
        return False

    cursor = connection.cursor()

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
            (%s, %s, %s, %s, %s, %s, %s)
        """, (
            claim_number,
            customer_id,
            policy_id,
            claim_amount,
            claim_date,
            description,
            "Pending"
        ))

        connection.commit()

        return True

    except Error as e:

        print("Add Claim Error:", e)

        return False

    finally:

        cursor.close()
        connection.close()


def get_claims():

    connection = get_connection()

    if connection is None:
        return []

    cursor = connection.cursor(dictionary=True)

    try:

        cursor.execute("""
            SELECT
                claims.*,
                customers.name AS customer_name,
                policies.policy_number,
                policies.policy_name

            FROM claims

            LEFT JOIN customers
                ON claims.customer_id = customers.id

            LEFT JOIN policies
                ON claims.policy_id = policies.id

            ORDER BY claims.id DESC
        """)

        return cursor.fetchall()

    except Error as e:

        print("Get Claims Error:", e)

        return []

    finally:

        cursor.close()
        connection.close()


def update_claim_status(
    claim_id,
    status
):

    connection = get_connection()

    if connection is None:
        return False

    cursor = connection.cursor()

    try:

        cursor.execute("""
            UPDATE claims
            SET status = %s
            WHERE id = %s
        """, (
            status,
            claim_id
        ))

        connection.commit()

        return True

    except Error as e:

        print("Update Claim Error:", e)

        return False

    finally:

        cursor.close()
        connection.close()


# =========================================================
# PAYMENT MANAGEMENT
# =========================================================

def add_payment(
    payment_number,
    customer_id,
    policy_id,
    amount,
    payment_date,
    payment_method
):

    connection = get_connection()

    if connection is None:
        return False

    cursor = connection.cursor()

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
            (%s, %s, %s, %s, %s, %s, %s)
        """, (
            payment_number,
            customer_id,
            policy_id,
            amount,
            payment_date,
            payment_method,
            "Paid"
        ))

        connection.commit()

        return True

    except Error as e:

        print("Add Payment Error:", e)

        return False

    finally:

        cursor.close()
        connection.close()


def get_payments():

    connection = get_connection()

    if connection is None:
        return []

    cursor = connection.cursor(dictionary=True)

    try:

        cursor.execute("""
            SELECT
                payments.*,
                customers.name AS customer_name,
                policies.policy_number,
                policies.policy_name

            FROM payments

            LEFT JOIN customers
                ON payments.customer_id = customers.id

            LEFT JOIN policies
                ON payments.policy_id = policies.id

            ORDER BY payments.id DESC
        """)

        return cursor.fetchall()

    except Error as e:

        print("Get Payments Error:", e)

        return []

    finally:

        cursor.close()
        connection.close()


# =========================================================
# DASHBOARD STATISTICS
# =========================================================

def get_dashboard_stats():

    connection = get_connection()

    if connection is None:

        return {
            "customers": 0,
            "policies": 0,
            "claims": 0,
            "pending_claims": 0,
            "agents": 0,
            "revenue": 0
        }

    cursor = connection.cursor()

    try:

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


        return {
            "customers": customers,
            "policies": policies,
            "claims": claims,
            "pending_claims": pending_claims,
            "agents": agents,
            "revenue": float(revenue or 0)
        }

    except Error as e:

        print("Dashboard Error:", e)

        return {
            "customers": 0,
            "policies": 0,
            "claims": 0,
            "pending_claims": 0,
            "agents": 0,
            "revenue": 0
        }

    finally:

        cursor.close()
        connection.close()


# =========================================================
# POLICY CATEGORY REPORT
# =========================================================

def get_policy_categories():

    connection = get_connection()

    if connection is None:
        return []

    cursor = connection.cursor(dictionary=True)

    try:

        cursor.execute("""
            SELECT
                category,
                COUNT(*) AS total

            FROM policies

            GROUP BY category
        """)

        return cursor.fetchall()

    except Error as e:

        print("Policy Category Error:", e)

        return []

    finally:

        cursor.close()
        connection.close()


# =========================================================
# CLAIM STATUS REPORT
# =========================================================

def get_claim_status():

    connection = get_connection()

    if connection is None:
        return []

    cursor = connection.cursor(dictionary=True)

    try:

        cursor.execute("""
            SELECT
                status,
                COUNT(*) AS total

            FROM claims

            GROUP BY status
        """)

        return cursor.fetchall()

    except Error as e:

        print("Claim Status Error:", e)

        return []

    finally:

        cursor.close()
        connection.close()


# =========================================================
# MONTHLY REVENUE
# =========================================================

def get_monthly_revenue():

    connection = get_connection()

    if connection is None:
        return []

    cursor = connection.cursor(dictionary=True)

    try:

        cursor.execute("""
            SELECT
                DATE_FORMAT(payment_date, '%Y-%m') AS month,
                SUM(amount) AS revenue

            FROM payments

            WHERE status = 'Paid'

            GROUP BY DATE_FORMAT(payment_date, '%Y-%m')

            ORDER BY month
        """)

        return cursor.fetchall()

    except Error as e:

        print("Revenue Error:", e)

        return []

    finally:

        cursor.close()
        connection.close()
