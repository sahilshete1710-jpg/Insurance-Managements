import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import date

import database


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Smart Insurance Management System",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================================================
# INITIALIZE DATABASE
# =========================================================

database.init_db()


# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown("""
<style>

.main {
    background-color: #f5f7fb;
}

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0f172a, #1e293b);
}

[data-testid="stSidebar"] * {
    color: white;
}

h1, h2, h3 {
    font-weight: 700;
}

.dashboard-card {
    background: white;
    padding: 22px;
    border-radius: 15px;
    box-shadow: 0px 3px 15px rgba(0,0,0,0.08);
    margin-bottom: 15px;
}

.card-title {
    font-size: 14px;
    color: #64748b;
}

.card-value {
    font-size: 30px;
    font-weight: bold;
    color: #0f172a;
}

.login-box {
    background: white;
    padding: 35px;
    border-radius: 18px;
    box-shadow: 0px 5px 25px rgba(0,0,0,0.10);
}

.small-text {
    color: #64748b;
}

</style>
""", unsafe_allow_html=True)


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

    st.markdown("<br><br>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:

        st.markdown("""
        <div class="login-box">

        <h1 style="text-align:center;">
        🛡️ Smart Insurance
        </h1>

        <p style="text-align:center;color:#64748b;">
        Insurance Management System
        </p>

        </div>
        """, unsafe_allow_html=True)

        st.write("")

        username = st.text_input(
            "Username",
            placeholder="Enter username"
        )

        password = st.text_input(
            "Password",
            type="password",
            placeholder="Enter password"
        )

        if st.button(
            "🔐 Login",
            use_container_width=True,
            type="primary"
        ):

            user = database.authenticate_user(
                username,
                password
            )

            if user:

                st.session_state.logged_in = True
                st.session_state.user = user

                st.success("Login successful!")
                st.rerun()

            else:

                st.error(
                    "Invalid username or password."
                )

        st.info(
            "Default Login: admin / admin123"
        )


# =========================================================
# DASHBOARD
# =========================================================

def dashboard():

    st.title("📊 Dashboard")

    st.write(
        f"Welcome back, **{st.session_state.user['full_name']}**"
    )

    stats = database.get_dashboard_stats()

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.markdown(f"""
        <div class="dashboard-card">
        <div class="card-title">Total Customers</div>
        <div class="card-value">{stats['customers']}</div>
        👥
        </div>
        """, unsafe_allow_html=True)

    with col2:

        st.markdown(f"""
        <div class="dashboard-card">
        <div class="card-title">Active Policies</div>
        <div class="card-value">{stats['policies']}</div>
        📋
        </div>
        """, unsafe_allow_html=True)

    with col3:

        st.markdown(f"""
        <div class="dashboard-card">
        <div class="card-title">Pending Claims</div>
        <div class="card-value">{stats['pending_claims']}</div>
        📑
        </div>
        """, unsafe_allow_html=True)

    with col4:

        st.markdown(f"""
        <div class="dashboard-card">
        <div class="card-title">Revenue</div>
        <div class="card-value">₹{stats['revenue']:,.0f}</div>
        💰
        </div>
        """, unsafe_allow_html=True)

    st.divider()

    col1, col2 = st.columns(2)

    # POLICY CHART
    with col1:

        st.subheader("📋 Policy Categories")

        categories = database.get_policy_categories()

        if categories:

            df = pd.DataFrame(categories)

            fig = px.pie(
                df,
                names="category",
                values="total",
                hole=0.45
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        else:

            st.info(
                "No policy data available."
            )

    # CLAIM CHART
    with col2:

        st.subheader("📑 Claim Status")

        claims = database.get_claim_status()

        if claims:

            df = pd.DataFrame(claims)

            fig = px.bar(
                df,
                x="status",
                y="total",
                text="total"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        else:

            st.info(
                "No claim data available."
            )


# =========================================================
# CUSTOMERS
# =========================================================

def customers_page():

    st.title("👥 Customer Management")

    tab1, tab2 = st.tabs([
        "➕ Add Customer",
        "📋 Customer Records"
    ])

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
                    "Phone"
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
                "Add Customer",
                type="primary"
            )

            if submit:

                if not name:

                    st.error(
                        "Customer name is required."
                    )

                else:

                    database.add_customer(
                        name,
                        email,
                        phone,
                        address,
                        str(dob),
                        gender
                    )

                    st.success(
                        "Customer added successfully!"
                    )

                    st.rerun()

    with tab2:

        customers = database.get_customers()

        if customers:

            df = pd.DataFrame(customers)

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
# POLICIES
# =========================================================

def policies_page():

    st.title("📋 Insurance Policy Management")

    customers = database.get_customers()

    if not customers:

        st.warning(
            "Please add a customer before creating a policy."
        )

        return

    customer_options = {
        f"{c['name']} - ID {c['id']}": c["id"]
        for c in customers
    }

    tab1, tab2 = st.tabs([
        "➕ Add Policy",
        "📋 Policy Records"
    ])

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
                    "Category",
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
                    "Premium Amount",
                    min_value=0.0,
                    step=500.0
                )

                coverage = st.number_input(
                    "Coverage Amount",
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
                        "Expired",
                        "Pending",
                        "Cancelled"
                    ]
                )

            submit = st.form_submit_button(
                "Create Policy",
                type="primary"
            )

            if submit:

                if not policy_number or not policy_name:

                    st.error(
                        "Policy number and policy name are required."
                    )

                else:

                    result = database.add_policy(
                        policy_number,
                        customer_options[customer],
                        policy_name,
                        category,
                        premium,
                        coverage,
                        str(start_date),
                        str(end_date),
                        status
                    )

                    if result:

                        st.success(
                            "Policy created successfully!"
                        )

                        st.rerun()

                    else:

                        st.error(
                            "Policy number already exists."
                        )

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
# AGENTS
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
                "Add Agent",
                type="primary"
            )

            if submit:

                if not name:

                    st.error(
                        "Agent name is required."
                    )

                else:

                    database.add_agent(
                        name,
                        email,
                        phone,
                        specialization,
                        commission,
                        status
                    )

                    st.success(
                        "Agent added successfully!"
                    )

                    st.rerun()

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
# CLAIMS
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
        f"{c['name']} - ID {c['id']}": c["id"]
        for c in customers
    }

    policy_options = {
        f"{p['policy_number']} - {p['policy_name']}":
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
                "Claim Amount",
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
                "Submit Claim",
                type="primary"
            )

            if submit:

                result = database.add_claim(
                    claim_number,
                    customer_options[customer],
                    policy_options[policy],
                    claim_amount,
                    str(claim_date),
                    description
                )

                if result:

                    st.success(
                        "Claim submitted successfully!"
                    )

                    st.rerun()

                else:

                    st.error(
                        "Claim number already exists."
                    )

    with tab2:

        claims = database.get_claims()

        if claims:

            for claim in claims:

                with st.expander(
                    f"{claim['claim_number']} | "
                    f"{claim['customer_name']} | "
                    f"₹{claim['claim_amount']:,.2f}"
                ):

                    st.write(
                        f"**Policy:** "
                        f"{claim['policy_number']}"
                    )

                    st.write(
                        f"**Description:** "
                        f"{claim['description']}"
                    )

                    st.write(
                        f"**Date:** "
                        f"{claim['claim_date']}"
                    )

                    status = st.selectbox(
                        "Claim Status",
                        [
                            "Pending",
                            "Approved",
                            "Rejected",
                            "Under Review"
                        ],
                        index=[
                            "Pending",
                            "Approved",
                            "Rejected",
                            "Under Review"
                        ].index(claim["status"]),
                        key=f"status_{claim['id']}"
                    )

                    if st.button(
                        "Update Status",
                        key=f"update_{claim['id']}"
                    ):

                        database.update_claim_status(
                            claim["id"],
                            status
                        )

                        st.success(
                            "Claim status updated."
                        )

                        st.rerun()

        else:

            st.info(
                "No claims found."
            )


# =========================================================
# PAYMENTS
# =========================================================

def payments_page():

    st.title("💳 Premium Payment Management")

    customers = database.get_customers()
    policies = database.get_policies()

    if not customers or not policies:

        st.warning(
            "Please create customers and policies first."
        )

        return

    customer_options = {
        f"{c['name']} - ID {c['id']}": c["id"]
        for c in customers
    }

    policy_options = {
        f"{p['policy_number']} - {p['policy_name']}":
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
                "Payment Amount",
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
                "Record Payment",
                type="primary"
            )

            if submit:

                result = database.add_payment(
                    payment_number,
                    customer_options[customer],
                    policy_options[policy],
                    amount,
                    str(payment_date),
                    payment_method
                )

                if result:

                    st.success(
                        "Payment recorded successfully!"
                    )

                    st.rerun()

                else:

                    st.error(
                        "Payment number already exists."
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

    col1, col2, col3 = st.columns(3)

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
            "Revenue",
            f"₹{stats['revenue']:,.2f}"
        )

    st.divider()

    policies = database.get_policies()

    if policies:

        st.subheader(
            "Insurance Policy Report"
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

    st.divider()

    claims = database.get_claims()

    if claims:

        st.subheader(
            "Claims Report"
        )

        df_claims = pd.DataFrame(claims)

        st.dataframe(
            df_claims,
            use_container_width=True,
            hide_index=True
        )

        csv = df_claims.to_csv(
            index=False
        ).encode("utf-8")

        st.download_button(
            "⬇️ Download Claims Report",
            csv,
            "claims_report.csv",
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

    with col2:

        st.info(
            "Your account is protected by "
            "role-based authentication."
        )


# =========================================================
# MAIN APPLICATION
# =========================================================

def main_app():

    user = st.session_state.user

    # SIDEBAR

    with st.sidebar:

        st.markdown("""
        <h2 style="text-align:center;">
        🛡️ SIMS
        </h2>
        """, unsafe_allow_html=True)

        st.markdown(
            f"### 👤 {user['full_name']}"
        )

        st.caption(
            f"Role: {user['role']}"
        )

        st.divider()

        menu = st.radio(
            "Navigation",
            [
                "📊 Dashboard",
                "👥 Customers",
                "📋 Policies",
                "👨‍💼 Agents",
                "📑 Claims",
                "💳 Payments",
                "📈 Reports",
                "👤 Profile"
            ]
        )

        st.divider()

        if st.button(
            "🚪 Logout",
            use_container_width=True
        ):

            st.session_state.logged_in = False
            st.session_state.user = None

            st.rerun()

    # PAGE ROUTING

    if menu == "📊 Dashboard":

        dashboard()

    elif menu == "👥 Customers":

        customers_page()

    elif menu == "📋 Policies":

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


# =========================================================
# RUN APPLICATION
# =========================================================

if not st.session_state.logged_in:

    login_page()

else:

    main_app()