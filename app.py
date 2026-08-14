import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

import database


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Smart Insurance Management System",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================================================
# LOAD CSS
# =========================================================

def load_css():

    css_file = Path(__file__).parent / "assets" / "style.css"

    if css_file.exists():

        with open(
            css_file,
            "r",
            encoding="utf-8"
        ) as f:

            st.markdown(
                f"<style>{f.read()}</style>",
                unsafe_allow_html=True
            )

    else:

        st.warning(
            "style.css was not found. "
            "Please create assets/style.css."
        )


load_css()


# =========================================================
# DATABASE INITIALIZATION
# =========================================================

if "database_ready" not in st.session_state:

    try:

        database_ready = database.init_db()

        st.session_state.database_ready = database_ready

    except Exception as e:

        st.session_state.database_ready = False

        st.error(
            f"Database connection failed: {e}"
        )


# =========================================================
# SESSION STATE
# =========================================================

if "logged_in" not in st.session_state:

    st.session_state.logged_in = False


if "user" not in st.session_state:

    st.session_state.user = None


# =========================================================
# LOGIN PAGE
# =========================================================

def login_page():

    st.markdown(
        "<br><br>",
        unsafe_allow_html=True
    )

    left, center, right = st.columns(
        [1, 2, 1]
    )

    with center:

        st.markdown("""
        <div class="login-box">

            <div class="login-logo">
                🛡️
            </div>

            <h1 style="text-align:center;">
                Smart Insurance
            </h1>

            <p style="
                text-align:center;
                color:#64748b;
                font-size:16px;
            ">
                Insurance Management System
            </p>

        </div>
        """, unsafe_allow_html=True)

        st.write("")

        username = st.text_input(
            "👤 Username",
            placeholder="Enter username"
        )

        password = st.text_input(
            "🔐 Password",
            type="password",
            placeholder="Enter password"
        )

        login_button = st.button(
            "🚀 Login",
            use_container_width=True,
            type="primary"
        )

        if login_button:

            if not username or not password:

                st.error(
                    "Please enter username and password."
                )

            else:

                user = database.authenticate_user(
                    username,
                    password
                )

                if user:

                    st.session_state.logged_in = True
                    st.session_state.user = user

                    st.success(
                        "Login successful!"
                    )

                    st.rerun()

                else:

                    st.error(
                        "Invalid username or password."
                    )

        st.info(
            "Demo Login: admin / admin123"
        )


# =========================================================
# DASHBOARD
# =========================================================

def dashboard():

    user = st.session_state.user

    st.markdown("""
    <div class="welcome-banner">

        <h2 style="color:white !important;">
            Welcome Back 👋
        </h2>

        <p style="
            color:white;
            font-size:16px;
        ">
            Manage your insurance operations
            from one powerful dashboard.
        </p>

    </div>
    """, unsafe_allow_html=True)

    stats = database.get_dashboard_stats()

    # -----------------------------------------------------
    # STATISTICS
    # -----------------------------------------------------

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.markdown(f"""
        <div class="stat-card stat-blue">

            <div style="font-size:32px;">
                👥
            </div>

            <div style="font-size:14px;">
                Total Customers
            </div>

            <div style="
                font-size:32px;
                font-weight:800;
            ">
                {stats["customers"]}
            </div>

        </div>
        """, unsafe_allow_html=True)

    with col2:

        st.markdown(f"""
        <div class="stat-card stat-purple">

            <div style="font-size:32px;">
                🛡️
            </div>

            <div style="font-size:14px;">
                Total Policies
            </div>

            <div style="
                font-size:32px;
                font-weight:800;
            ">
                {stats["policies"]}
            </div>

        </div>
        """, unsafe_allow_html=True)

    with col3:

        st.markdown(f"""
        <div class="stat-card stat-pink">

            <div style="font-size:32px;">
                📑
            </div>

            <div style="font-size:14px;">
                Pending Claims
            </div>

            <div style="
                font-size:32px;
                font-weight:800;
            ">
                {stats["pending_claims"]}
            </div>

        </div>
        """, unsafe_allow_html=True)

    with col4:

        st.markdown(f"""
        <div class="stat-card stat-green">

            <div style="font-size:32px;">
                💰
            </div>

            <div style="font-size:14px;">
                Total Revenue
            </div>

            <div style="
                font-size:27px;
                font-weight:800;
            ">
                ₹{stats["revenue"]:,.0f}
            </div>

        </div>
        """, unsafe_allow_html=True)

    st.write("")

    # -----------------------------------------------------
    # CHARTS
    # -----------------------------------------------------

    col1, col2 = st.columns(2)

    with col1:

        st.subheader("📊 Policy Categories")

        categories = database.get_policy_categories()

        if categories:

            df = pd.DataFrame(categories)

            fig = px.pie(
                df,
                names="category",
                values="total",
                hole=0.50,
                title="Insurance Policy Distribution"
            )

            fig.update_layout(
                margin=dict(
                    l=20,
                    r=20,
                    t=50,
                    b=20
                )
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        else:

            st.info(
                "No policy data available yet."
            )

    with col2:

        st.subheader("📑 Claim Status")

        claim_status = database.get_claim_status()

        if claim_status:

            df = pd.DataFrame(claim_status)

            fig = px.bar(
                df,
                x="status",
                y="total",
                text="total",
                title="Claim Status Overview"
            )

            fig.update_layout(
                margin=dict(
                    l=20,
                    r=20,
                    t=50,
                    b=20
                )
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        else:

            st.info(
                "No claim data available yet."
            )

    # -----------------------------------------------------
    # REVENUE CHART
    # -----------------------------------------------------

    st.subheader("💰 Monthly Revenue")

    revenue = database.get_monthly_revenue()

    if revenue:

        df = pd.DataFrame(revenue)

        fig = px.line(
            df,
            x="month",
            y="revenue",
            markers=True,
            title="Monthly Premium Revenue"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    else:

        st.info(
            "No payment data available yet."
        )


# =========================================================
# CUSTOMER PAGE
# =========================================================

def customers_page():

    st.title("👥 Customer Management")

    tab1, tab2 = st.tabs([
        "➕ Add Customer",
        "📋 Customer Records"
    ])

    # -----------------------------------------------------
    # ADD CUSTOMER
    # -----------------------------------------------------

    with tab1:

        with st.form("customer_form"):

            col1, col2 = st.columns(2)

            with col1:

                name = st.text_input(
                    "Full Name *"
                )

                email = st.text_input(
                    "Email"
                )

                phone = st.text_input(
                    "Phone Number"
                )

            with col2:

                dob = st.date_input(
                    "Date of Birth"
                )

                gender = st.selectbox(
                    "Gender",
                    [
                        "Male",
                        "Female",
                        "Other"
                    ]
                )

                address = st.text_area(
                    "Address"
                )

            submit = st.form_submit_button(
                "💾 Save Customer",
                type="primary"
            )

            if submit:

                if not name.strip():

                    st.error(
                        "Customer name is required."
                    )

                else:

                    success = database.add_customer(
                        name,
                        email,
                        phone,
                        address,
                        dob,
                        gender
                    )

                    if success:

                        st.success(
                            "Customer saved to MySQL successfully!"
                        )

                        st.rerun()

                    else:

                        st.error(
                            "Could not save customer."
                        )

    # -----------------------------------------------------
    # CUSTOMER RECORDS
    # -----------------------------------------------------

    with tab2:

        customers = database.get_customers()

        if customers:

            df = pd.DataFrame(customers)

            search = st.text_input(
                "🔎 Search Customer"
            )

            if search:

                mask = df.astype(
                    str
                ).apply(
                    lambda row:
                    row.str.contains(
                        search,
                        case=False,
                        na=False
                    ).any(),
                    axis=1
                )

                df = df[mask]

            st.dataframe(
                df,
                use_container_width=True,
                hide_index=True
            )

        else:

            st.info(
                "No customers found."
            )


# =========================================================
# POLICY PAGE
# =========================================================

def policies_page():

    st.title("🛡️ Insurance Policy Management")

    customers = database.get_customers()

    if not customers:

        st.warning(
            "Please add a customer before creating a policy."
        )

        return

    customer_options = {
        f"{c['name']} — ID {c['id']}":
        c["id"]

        for c in customers
    }

    tab1, tab2 = st.tabs([
        "➕ Create Policy",
        "📋 Policy Records"
    ])

    # -----------------------------------------------------
    # CREATE POLICY
    # -----------------------------------------------------

    with tab1:

        with st.form("policy_form"):

            col1, col2 = st.columns(2)

            with col1:

                policy_number = st.text_input(
                    "Policy Number *",
                    placeholder="POL-1001"
                )

                policy_name = st.text_input(
                    "Policy Name *",
                    placeholder="Health Insurance"
                )

                category = st.selectbox(
                    "Policy Category",
                    [
                        "Life Insurance",
                        "Health Insurance",
                        "Vehicle Insurance",
                        "Travel Insurance",
                        "Home Insurance",
                        "Education Insurance"
                    ]
                )

                customer = st.selectbox(
                    "Customer",
                    list(customer_options.keys())
                )

            with col2:

                premium = st.number_input(
                    "Premium Amount ₹",
                    min_value=0.0,
                    step=500.0
                )

                coverage = st.number_input(
                    "Coverage Amount ₹",
                    min_value=0.0,
                    step=10000.0
                )

                start_date = st.date_input(
                    "Start Date"
                )

                end_date = st.date_input(
                    "End Date"
                )

                status = st.selectbox(
                    "Status",
                    [
                        "Active",
                        "Pending",
                        "Expired",
                        "Cancelled"
                    ]
                )

            submit = st.form_submit_button(
                "🛡️ Create Policy",
                type="primary"
            )

            if submit:

                if not policy_number.strip():

                    st.error(
                        "Policy number is required."
                    )

                elif not policy_name.strip():

                    st.error(
                        "Policy name is required."
                    )

                elif end_date < start_date:

                    st.error(
                        "End date cannot be before start date."
                    )

                else:

                    success = database.add_policy(
                        policy_number,
                        customer_options[customer],
                        policy_name,
                        category,
                        premium,
                        coverage,
                        start_date,
                        end_date,
                        status
                    )

                    if success:

                        st.success(
                            "Policy saved to MySQL successfully!"
                        )

                        st.rerun()

                    else:

                        st.error(
                            "Policy number may already exist."
                        )

    # -----------------------------------------------------
    # POLICY RECORDS
    # -----------------------------------------------------

    with tab2:

        policies = database.get_policies()

        if policies:

            df = pd.DataFrame(policies)

            st.dataframe(
                df,
                use_container_width=True,
                hide_index=True
            )

        else:

            st.info(
                "No policies found."
            )


# =========================================================
# AGENT PAGE
# =========================================================

def agents_page():

    st.title("👨‍💼 Agent Management")

    tab1, tab2 = st.tabs([
        "➕ Add Agent",
        "📋 Agent Records"
    ])

    with tab1:

        with st.form("agent_form"):

            col1, col2 = st.columns(2)

            with col1:

                name = st.text_input(
                    "Agent Name *"
                )

                email = st.text_input(
                    "Email"
                )

                phone = st.text_input(
                    "Phone"
                )

            with col2:

                specialization = st.selectbox(
                    "Specialization",
                    [
                        "Life Insurance",
                        "Health Insurance",
                        "Vehicle Insurance",
                        "General Insurance"
                    ]
                )

                commission = st.number_input(
                    "Commission (%)",
                    min_value=0.0,
                    max_value=100.0,
                    value=5.0
                )

                status = st.selectbox(
                    "Status",
                    [
                        "Active",
                        "Inactive"
                    ]
                )

            submit = st.form_submit_button(
                "💾 Save Agent",
                type="primary"
            )

            if submit:

                if not name.strip():

                    st.error(
                        "Agent name is required."
                    )

                else:

                    success = database.add_agent(
                        name,
                        email,
                        phone,
                        specialization,
                        commission,
                        status
                    )

                    if success:

                        st.success(
                            "Agent saved to MySQL successfully!"
                        )

                        st.rerun()

                    else:

                        st.error(
                            "Could not save agent."
                        )

    with tab2:

        agents = database.get_agents()

        if agents:

            df = pd.DataFrame(agents)

            st.dataframe(
                df,
                use_container_width=True,
                hide_index=True
            )

        else:

            st.info(
                "No agents found."
            )


# =========================================================
# CLAIM PAGE
# =========================================================

def claims_page():

    st.title("📑 Claim Management")

    customers = database.get_customers()
    policies = database.get_policies()

    if not customers:

        st.warning(
            "Please add customers first."
        )

        return

    if not policies:

        st.warning(
            "Please create a policy first."
        )

        return

    customer_options = {
        f"{c['name']} — ID {c['id']}":
        c["id"]

        for c in customers
    }

    policy_options = {
        f"{p['policy_number']} — {p['policy_name']}":
        p["id"]

        for p in policies
    }

    tab1, tab2 = st.tabs([
        "➕ Submit Claim",
        "📋 Claim Records"
    ])

    with tab1:

        with st.form("claim_form"):

            claim_number = st.text_input(
                "Claim Number *",
                placeholder="CLM-1001"
            )

            customer = st.selectbox(
                "Customer",
                list(customer_options.keys())
            )

            policy = st.selectbox(
                "Policy",
                list(policy_options.keys())
            )

            claim_amount = st.number_input(
                "Claim Amount ₹",
                min_value=0.0,
                step=1000.0
            )

            claim_date = st.date_input(
                "Claim Date"
            )

            description = st.text_area(
                "Claim Description"
            )

            submit = st.form_submit_button(
                "📤 Submit Claim",
                type="primary"
            )

            if submit:

                if not claim_number.strip():

                    st.error(
                        "Claim number is required."
                    )

                else:

                    success = database.add_claim(
                        claim_number,
                        customer_options[customer],
                        policy_options[policy],
                        claim_amount,
                        claim_date,
                        description
                    )

                    if success:

                        st.success(
                            "Claim saved to MySQL successfully!"
                        )

                        st.rerun()

                    else:

                        st.error(
                            "Claim number may already exist."
                        )

    with tab2:

        claims = database.get_claims()

        if claims:

            for claim in claims:

                title = (
                    f"📑 {claim['claim_number']}  |  "
                    f"{claim['customer_name'] or 'Unknown'}  |  "
                    f"₹{float(claim['claim_amount']):,.0f}"
                )

                with st.expander(title):

                    col1, col2 = st.columns(2)

                    with col1:

                        st.write(
                            f"**Policy:** "
                            f"{claim['policy_number'] or 'N/A'}"
                        )

                        st.write(
                            f"**Date:** "
                            f"{claim['claim_date']}"
                        )

                    with col2:

                        st.write(
                            f"**Amount:** "
                            f"₹{float(claim['claim_amount']):,.2f}"
                        )

                        st.write(
                            f"**Description:** "
                            f"{claim['description'] or 'N/A'}"
                        )

                    status_options = [
                        "Pending",
                        "Under Review",
                        "Approved",
                        "Rejected"
                    ]

                    current_status = claim["status"]

                    if current_status not in status_options:

                        current_status = "Pending"

                    status = st.selectbox(
                        "Claim Status",
                        status_options,
                        index=status_options.index(
                            current_status
                        ),
                        key=f"claim_status_{claim['id']}"
                    )

                    if st.button(
                        "💾 Update Status",
                        key=f"update_claim_{claim['id']}"
                    ):

                        success = database.update_claim_status(
                            claim["id"],
                            status
                        )

                        if success:

                            st.success(
                                "Claim status updated in MySQL."
                            )

                            st.rerun()

        else:

            st.info(
                "No claims found."
            )


# =========================================================
# PAYMENT PAGE
# =========================================================

def payments_page():

    st.title("💳 Premium Payment Management")

    customers = database.get_customers()
    policies = database.get_policies()

    if not customers:

        st.warning(
            "Please add customers first."
        )

        return

    if not policies:

        st.warning(
            "Please create policies first."
        )

        return

    customer_options = {
        f"{c['name']} — ID {c['id']}":
        c["id"]

        for c in customers
    }

    policy_options = {
        f"{p['policy_number']} — {p['policy_name']}":
        p["id"]

        for p in policies
    }

    tab1, tab2 = st.tabs([
        "➕ Record Payment",
        "📋 Payment History"
    ])

    with tab1:

        with st.form("payment_form"):

            payment_number = st.text_input(
                "Payment Number *",
                placeholder="PAY-1001"
            )

            customer = st.selectbox(
                "Customer",
                list(customer_options.keys())
            )

            policy = st.selectbox(
                "Policy",
                list(policy_options.keys())
            )

            amount = st.number_input(
                "Payment Amount ₹",
                min_value=0.0,
                step=500.0
            )

            payment_date = st.date_input(
                "Payment Date"
            )

            payment_method = st.selectbox(
                "Payment Method",
                [
                    "Cash",
                    "UPI",
                    "Credit Card",
                    "Debit Card",
                    "Net Banking"
                ]
            )

            submit = st.form_submit_button(
                "💳 Save Payment",
                type="primary"
            )

            if submit:

                if not payment_number.strip():

                    st.error(
                        "Payment number is required."
                    )

                elif amount <= 0:

                    st.error(
                        "Payment amount must be greater than zero."
                    )

                else:

                    success = database.add_payment(
                        payment_number,
                        customer_options[customer],
                        policy_options[policy],
                        amount,
                        payment_date,
                        payment_method
                    )

                    if success:

                        st.success(
                            "Payment saved to MySQL successfully!"
                        )

                        st.rerun()

                    else:

                        st.error(
                            "Payment number may already exist."
                        )

    with tab2:

        payments = database.get_payments()

        if payments:

            df = pd.DataFrame(payments)

            st.dataframe(
                df,
                use_container_width=True,
                hide_index=True
            )

            total = sum(
                float(p["amount"])
                for p in payments
            )

            st.metric(
                "Total Recorded Payments",
                f"₹{total:,.2f}"
            )

        else:

            st.info(
                "No payment records found."
            )


# =========================================================
# REPORTS
# =========================================================

def reports_page():

    st.title("📊 Reports & Analytics")

    stats = database.get_dashboard_stats()

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            "Customers",
            stats["customers"]
        )

    with col2:

        st.metric(
            "Policies",
            stats["policies"]
        )

    with col3:

        st.metric(
            "Claims",
            stats["claims"]
        )

    with col4:

        st.metric(
            "Revenue",
            f"₹{stats['revenue']:,.0f}"
        )

    st.divider()

    # -----------------------------------------------------
    # POLICY REPORT
    # -----------------------------------------------------

    policies = database.get_policies()

    if policies:

        st.subheader(
            "🛡️ Insurance Policy Report"
        )

        df = pd.DataFrame(policies)

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )

        csv = df.to_csv(
            index=False
        ).encode("utf-8")

        st.download_button(
            "⬇️ Download Policy Report",
            csv,
            "policy_report.csv",
            "text/csv"
        )

    # -----------------------------------------------------
    # CLAIM REPORT
    # -----------------------------------------------------

    claims = database.get_claims()

    if claims:

        st.subheader(
            "📑 Claims Report"
        )

        df = pd.DataFrame(claims)

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )

        csv = df.to_csv(
            index=False
        ).encode("utf-8")

        st.download_button(
            "⬇️ Download Claims Report",
            csv,
            "claims_report.csv",
            "text/csv"
        )

    # -----------------------------------------------------
    # PAYMENT REPORT
    # -----------------------------------------------------

    payments = database.get_payments()

    if payments:

        st.subheader(
            "💳 Payment Report"
        )

        df = pd.DataFrame(payments)

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )

        csv = df.to_csv(
            index=False
        ).encode("utf-8")

        st.download_button(
            "⬇️ Download Payment Report",
            csv,
            "payment_report.csv",
            "text/csv"
        )


# =========================================================
# PROFILE
# =========================================================

def profile_page():

    st.title("👤 My Profile")

    user = st.session_state.user

    col1, col2 = st.columns(2)

    with col1:

        st.markdown(
            '<div class="glass-card">',
            unsafe_allow_html=True
        )

        st.subheader(
            "Account Information"
        )

        st.write(
            f"**Name:** {user['full_name']}"
        )

        st.write(
            f"**Username:** {user['username']}"
        )

        st.write(
            f"**Role:** {user['role']}"
        )

        st.write(
            f"**Email:** {user['email']}"
        )

        st.markdown(
            "</div>",
            unsafe_allow_html=True
        )

    with col2:

        st.info(
            "🔐 Your account is protected "
            "by password authentication."
        )


# =========================================================
# ADMIN USER MANAGEMENT
# =========================================================

def users_page():

    st.title("👤 User Management")

    tab1, tab2 = st.tabs([
        "➕ Add User",
        "📋 Users"
    ])

    with tab1:

        with st.form("user_form"):

            col1, col2 = st.columns(2)

            with col1:

                username = st.text_input(
                    "Username *"
                )

                full_name = st.text_input(
                    "Full Name *"
                )

                email = st.text_input(
                    "Email"
                )

            with col2:

                password = st.text_input(
                    "Password *",
                    type="password"
                )

                role = st.selectbox(
                    "Role",
                    [
                        "Admin",
                        "Agent",
                        "Customer"
                    ]
                )

            submit = st.form_submit_button(
                "➕ Create User",
                type="primary"
            )

            if submit:

                if (
                    not username.strip()
                    or not password
                    or not full_name.strip()
                ):

                    st.error(
                        "Please fill all required fields."
                    )

                else:

                    success = database.add_user(
                        username,
                        password,
                        full_name,
                        role,
                        email
                    )

                    if success:

                        st.success(
                            "User created successfully."
                        )

                        st.rerun()

                    else:

                        st.error(
                            "Username already exists."
                        )

    with tab2:

        users = database.get_users()

        if users:

            df = pd.DataFrame(users)

            st.dataframe(
                df,
                use_container_width=True,
                hide_index=True
            )

        else:

            st.info(
                "No users found."
            )


# =========================================================
# MAIN APPLICATION
# =========================================================

def main_app():

    user = st.session_state.user

    # -----------------------------------------------------
    # SIDEBAR
    # -----------------------------------------------------

    with st.sidebar:

        st.markdown("""
        <div style="
            text-align:center;
            padding:10px;
        ">

            <div style="
                font-size:45px;
            ">
                🛡️
            </div>

            <h2 style="
                color:white !important;
                margin:0;
            ">
                SIMS
            </h2>

            <p style="
                color:#c7d2fe;
                font-size:12px;
            ">
                Smart Insurance
            </p>

        </div>
        """, unsafe_allow_html=True)

        st.divider()

        st.markdown(
            f"""
            <div style="
                background:rgba(255,255,255,0.08);
                padding:12px;
                border-radius:14px;
            ">

                <b>👤 {user['full_name']}</b>

                <br>

                <small>
                    Role: {user['role']}
                </small>

            </div>
            """,
            unsafe_allow_html=True
        )

        st.divider()

        menu_items = [
            "📊 Dashboard",
            "👥 Customers",
            "🛡️ Policies",
            "👨‍💼 Agents",
            "📑 Claims",
            "💳 Payments",
            "📈 Reports",
            "👤 Profile"
        ]

        if user["role"] == "Admin":

            menu_items.insert(
                7,
                "⚙️ User Management"
            )

        menu = st.radio(
            "Navigation",
            menu_items
        )

        st.divider()

        if st.button(
            "🚪 Logout",
            use_container_width=True
        ):

            st.session_state.logged_in = False
            st.session_state.user = None

            st.rerun()

    # -----------------------------------------------------
    # ROUTING
    # -----------------------------------------------------

    if menu == "📊 Dashboard":

        dashboard()

    elif menu == "👥 Customers":

        customers_page()

    elif menu == "🛡️ Policies":

        policies_page()

    elif menu == "👨‍💼 Agents":

        agents_page()

    elif menu == "📑 Claims":

        claims_page()

    elif menu == "💳 Payments":

        payments_page()

    elif menu == "📈 Reports":

        reports_page()

    elif menu == "👤 Profile":

        profile_page()

    elif menu == "⚙️ User Management":

        users_page()


# =========================================================
# APPLICATION START
# =========================================================

if not st.session_state.get(
    "database_ready",
    False
):

    st.error("""
    ❌ MySQL database connection failed.

    Please check:

    1. MySQL Server is running.
    2. Database insurance_management exists.
    3. MySQL username is correct.
    4. MySQL password is correct.
    5. mysql-connector-python is installed.
    """)

    st.stop()


if not st.session_state.logged_in:

    login_page()

else:

    main_app()
