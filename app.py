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
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

:root {
    --ink:#0f172a;
    --muted:#64748b;
    --purple:#6d28d9;
    --indigo:#4f46e5;
    --cyan:#0891b2;
    --pink:#db2777;
    --green:#059669;
    --orange:#ea580c;
}

html, body, [class*="css"] {
    font-family:'Inter',sans-serif;
}

.stApp {
    background:
      radial-gradient(circle at 5% 0%, rgba(124,58,237,.12), transparent 23%),
      radial-gradient(circle at 96% 4%, rgba(6,182,212,.12), transparent 22%),
      linear-gradient(135deg,#f8fafc 0%,#f5f3ff 45%,#ecfeff 100%);
}

.block-container {
    max-width:1500px;
    padding:1.35rem 2rem 3rem;
}

[data-testid="stSidebar"] {
    background:
      radial-gradient(circle at 20% 10%,rgba(129,140,248,.22),transparent 25%),
      linear-gradient(180deg,#0b1026 0%,#151b45 48%,#312e81 100%);
    border-right:1px solid rgba(255,255,255,.08);
}

[data-testid="stSidebar"] * { color:#fff !important; }

[data-testid="stSidebar"] .stRadio > div {
    gap:6px;
}

[data-testid="stSidebar"] .stRadio label {
    padding:8px 10px;
    border-radius:12px;
    transition:.2s;
}

[data-testid="stSidebar"] .stRadio label:hover {
    background:rgba(255,255,255,.12);
}

.brand-premium {
    text-align:center;
    padding:6px 6px 20px;
}

.brand-shield {
    width:68px;
    height:68px;
    margin:0 auto 10px;
    display:flex;
    align-items:center;
    justify-content:center;
    border-radius:22px;
    background:linear-gradient(135deg,#818cf8,#22d3ee);
    box-shadow:0 12px 30px rgba(34,211,238,.22);
    font-size:36px;
}

.brand-title {
    font-size:19px;
    font-weight:800;
    letter-spacing:.5px;
}

.brand-sub {
    font-size:10px;
    opacity:.6;
    letter-spacing:2px;
}

.hero-premium {
    position:relative;
    overflow:hidden;
    padding:30px 34px;
    border-radius:28px;
    color:#fff;
    background:
      radial-gradient(circle at 82% 20%,rgba(255,255,255,.25),transparent 16%),
      radial-gradient(circle at 96% 100%,rgba(34,211,238,.32),transparent 30%),
      linear-gradient(115deg,#312e81,#4f46e5 42%,#0891b2);
    box-shadow:0 24px 60px rgba(49,46,129,.24);
    margin-bottom:24px;
}

.hero-premium:after {
    content:"";
    position:absolute;
    width:210px;
    height:210px;
    right:-70px;
    top:-80px;
    border-radius:50%;
    border:35px solid rgba(255,255,255,.08);
}

.hero-kicker {
    font-size:12px;
    text-transform:uppercase;
    letter-spacing:2px;
    opacity:.72;
    font-weight:700;
}

.hero-premium h1 {
    margin:5px 0 7px;
    font-size:32px;
    font-weight:800;
}

.hero-premium p {
    margin:0;
    opacity:.82;
}

.kpi-premium {
    position:relative;
    overflow:hidden;
    min-height:150px;
    padding:20px;
    border-radius:22px;
    background:rgba(255,255,255,.92);
    border:1px solid rgba(255,255,255,.95);
    box-shadow:0 12px 32px rgba(15,23,42,.07);
}

.kpi-premium:before {
    content:"";
    position:absolute;
    left:0;
    top:0;
    bottom:0;
    width:5px;
    background:var(--accent,#4f46e5);
}

.kpi-icon-premium {
    width:45px;
    height:45px;
    display:flex;
    align-items:center;
    justify-content:center;
    border-radius:14px;
    background:var(--soft,#eef2ff);
    font-size:23px;
}

.kpi-label-premium {
    color:#64748b;
    font-size:12px;
    font-weight:600;
    margin-top:12px;
}

.kpi-value-premium {
    color:#0f172a;
    font-size:27px;
    font-weight:800;
    margin-top:2px;
}

.kpi-trend {
    color:#059669;
    font-size:11px;
    font-weight:700;
    margin-top:4px;
}

.section-premium {
    background:rgba(255,255,255,.88);
    border:1px solid rgba(226,232,240,.8);
    border-radius:22px;
    padding:20px;
    margin-top:20px;
    box-shadow:0 12px 35px rgba(15,23,42,.055);
}

.section-title {
    font-size:17px;
    font-weight:800;
    color:#111827;
    margin-bottom:2px;
}

.section-sub {
    font-size:12px;
    color:#94a3b8;
    margin-bottom:15px;
}

.page-title-premium {
    font-size:31px;
    line-height:1.1;
    font-weight:800;
    color:#111827;
    margin-bottom:5px;
}

.page-sub-premium {
    color:#64748b;
    margin-bottom:22px;
}

.login-shell {
    max-width:480px;
    margin:7vh auto 0;
}

.login-card-premium {
    padding:38px;
    border-radius:28px;
    background:rgba(255,255,255,.94);
    border:1px solid rgba(255,255,255,.9);
    box-shadow:0 30px 80px rgba(49,46,129,.18);
    backdrop-filter:blur(18px);
}

.login-icon {
    width:82px;
    height:82px;
    display:flex;
    align-items:center;
    justify-content:center;
    margin:0 auto 16px;
    border-radius:26px;
    background:linear-gradient(135deg,#4f46e5,#06b6d4);
    box-shadow:0 16px 35px rgba(79,70,229,.28);
    font-size:43px;
}

.login-title {
    text-align:center;
    font-size:30px;
    font-weight:800;
    color:#111827;
}

.login-sub {
    text-align:center;
    color:#64748b;
    margin:5px 0 25px;
}

.stButton > button {
    border-radius:13px;
    min-height:43px;
    font-weight:700;
    transition:.2s;
}

.stButton > button:hover {
    transform:translateY(-1px);
    box-shadow:0 8px 20px rgba(79,70,229,.16);
}

div[data-testid="stMetric"] {
    background:rgba(255,255,255,.9);
    border:1px solid #eef2ff;
    border-radius:16px;
    box-shadow:0 8px 25px rgba(15,23,42,.05);
}

[data-testid="stDataFrame"] {
    border-radius:15px;
    overflow:hidden;
}

div[data-baseweb="tab-list"] {
    gap:8px;
}

button[data-baseweb="tab"] {
    border-radius:10px;
    font-weight:700;
}

.insight {
    padding:15px 17px;
    border-radius:16px;
    background:linear-gradient(135deg,#eef2ff,#ecfeff);
    border:1px solid #dbeafe;
    color:#334155;
    font-size:13px;
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

    st.markdown("""
    <div class="login-shell">
        <div class="login-card-premium">
            <div class="login-icon">🛡️</div>
            <div class="login-title">Smart Insurance</div>
            <div class="login-sub">Premium Insurance Management Platform</div>
    """, unsafe_allow_html=True)

    username = st.text_input("Username", placeholder="Enter username")
    password = st.text_input("Password", type="password", placeholder="Enter password")

    if st.button("🔐  Sign In Securely", use_container_width=True, type="primary"):
        user = database.authenticate_user(username, password)
        if user:
            st.session_state.logged_in = True
            st.session_state.user = user
            st.success("Login successful!")
            st.rerun()
        else:
            st.error("Invalid username or password.")

    st.info("Demo Login  •  admin / admin123")
    st.markdown("</div></div>", unsafe_allow_html=True)


# =========================================================
# DASHBOARD
# =========================================================

def dashboard():

    stats = database.get_dashboard_stats()
    user = st.session_state.user

    st.markdown(f"""
    <div class="hero-premium">
        <div class="hero-kicker">Smart Insurance • Executive Dashboard</div>
        <h1>Welcome back, {user['full_name']} 👋</h1>
        <p>Everything you need to monitor policies, claims, customers and premium revenue.</p>
    </div>
    """, unsafe_allow_html=True)

    cards = [
        ("👥","Total Customers",f"{stats['customers']:,}","#4f46e5","#eef2ff","Live records"),
        ("🛡️","Active Policies",f"{stats['policies']:,}","#0891b2","#ecfeff","Policy portfolio"),
        ("📑","Pending Claims",f"{stats['pending_claims']:,}","#ea580c","#fff7ed","Needs attention"),
        ("💰","Total Revenue",f"₹{stats['revenue']:,.0f}","#059669","#ecfdf5","Paid premiums")
    ]

    cols = st.columns(4)
    for col, (icon,label,value,accent,soft,note) in zip(cols,cards):
        with col:
            st.markdown(f"""
            <div class="kpi-premium" style="--accent:{accent};">
                <div class="kpi-icon-premium" style="--soft:{soft};">{icon}</div>
                <div class="kpi-label-premium">{label}</div>
                <div class="kpi-value-premium">{value}</div>
                <div class="kpi-trend">● {note}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("""
    <div class="section-premium">
        <div class="section-title">📌 Portfolio Intelligence</div>
        <div class="section-sub">A quick visual summary of your insurance business.</div>
    </div>
    """, unsafe_allow_html=True)

    c1, c2 = st.columns(2)

    with c1:
        st.markdown('<div class="section-premium">', unsafe_allow_html=True)
        st.subheader("🛡️ Policy Portfolio")
        categories = database.get_policy_categories()
        if categories:
            df = pd.DataFrame(categories)
            fig = px.pie(
                df, names="category", values="total", hole=.62,
                template="plotly_white"
            )
            fig.update_traces(
                textposition="outside",
                textinfo="percent+label",
                marker=dict(line=dict(color="white", width=3))
            )
            fig.update_layout(
                height=350,
                margin=dict(l=10,r=10,t=10,b=10),
                showlegend=False,
                paper_bgcolor="rgba(0,0,0,0)"
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Add policies to unlock portfolio analytics.")
        st.markdown('</div>', unsafe_allow_html=True)

    with c2:
        st.markdown('<div class="section-premium">', unsafe_allow_html=True)
        st.subheader("📑 Claims Overview")
        claims = database.get_claim_status()
        if claims:
            df = pd.DataFrame(claims)
            fig = px.bar(
                df, x="status", y="total", text="total",
                template="plotly_white"
            )
            fig.update_traces(
                textposition="outside",
                marker_line_width=0
            )
            fig.update_layout(
                height=350,
                margin=dict(l=10,r=10,t=10,b=10),
                paper_bgcolor="rgba(0,0,0,0)",
                xaxis_title="",
                yaxis_title="Claims"
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No claims available yet.")
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="section-premium">', unsafe_allow_html=True)
    st.subheader("💹 Premium Revenue Trend")
    revenue = database.get_monthly_revenue()
    if revenue:
        df = pd.DataFrame(revenue)
        fig = px.area(
            df, x="month", y="revenue", markers=True,
            template="plotly_white"
        )
        fig.update_traces(line_width=3)
        fig.update_layout(
            height=330,
            margin=dict(l=10,r=10,t=10,b=10),
            paper_bgcolor="rgba(0,0,0,0)",
            xaxis_title="",
            yaxis_title="Revenue (₹)"
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.markdown(
            '<div class="insight">💡 Record your first premium payment to see the live revenue trend here.</div>',
            unsafe_allow_html=True
        )
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="section-premium">', unsafe_allow_html=True)
    a,b,c = st.columns(3)
    a.metric("👨‍💼 Agents", stats["agents"])
    b.metric("📋 Total Claims", stats["claims"])
    c.metric("⚡ Pending Ratio",
             f"{(stats['pending_claims']/stats['claims']*100):.1f}%"
             if stats["claims"] else "0%")
    st.markdown('</div>', unsafe_allow_html=True)


# =========================================================
# CUSTOMERS
# =========================================================

def customers_page():

    st.markdown('<div class="page-title-premium">👥 Customer Management</div><div class="page-sub-premium">Create, search and manage your insurance customers.</div>', unsafe_allow_html=True)

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

    st.markdown('<div class="page-title-premium">🛡️ Insurance Policy Management</div><div class="page-sub-premium">Create and monitor your insurance policy portfolio.</div>', unsafe_allow_html=True)

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

    st.markdown('<div class="page-title-premium">👨‍💼 Agent Management</div><div class="page-sub-premium">Manage agents, specializations and commissions.</div>', unsafe_allow_html=True)

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

    st.markdown('<div class="page-title-premium">📑 Claim Management</div><div class="page-sub-premium">Submit, review and update insurance claims.</div>', unsafe_allow_html=True)

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

    st.markdown('<div class="page-title-premium">💳 Premium Payments</div><div class="page-sub-premium">Record premium payments and monitor transaction history.</div>', unsafe_allow_html=True)

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

    st.markdown('<div class="page-title-premium">📈 Reports & Analytics</div><div class="page-sub-premium">Explore live insurance performance and export reports.</div>', unsafe_allow_html=True)

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

    st.markdown('<div class="page-title-premium">👤 My Profile</div><div class="page-sub-premium">Account and secure access information.</div>', unsafe_allow_html=True)

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
        <div class="brand-premium">
            <div class="brand-shield">🛡️</div>
            <div class="brand-title">SMART INSURANCE</div>
            <div class="brand-sub">MANAGEMENT SYSTEM</div>
        </div>
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