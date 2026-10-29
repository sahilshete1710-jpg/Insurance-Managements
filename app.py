import random
from datetime import date, timedelta

import mysql.connector
from flask import (Flask, abort, flash, redirect, render_template, request,
                   session, url_for)
from mysql.connector import Error
from werkzeug.security import check_password_hash, generate_password_hash

from config import DB_CONFIG, SECRET_KEY

app = Flask(__name__)
app.secret_key = SECRET_KEY


# ---------------------------------------------------------------- helpers
def run(sql, params=(), fetch=None):
    """fetch: None (write -> returns lastrowid), 'one', or 'all'."""
    conn = mysql.connector.connect(**DB_CONFIG)
    cur = conn.cursor(dictionary=True)
    try:
        cur.execute(sql, params)
        if fetch == "one":
            return cur.fetchone()
        if fetch == "all":
            return cur.fetchall()
        conn.commit()
        return cur.lastrowid
    finally:
        cur.close()
        conn.close()


@app.template_filter("money")
def money(v):
    return f"₹{float(v or 0):,.2f}"


@app.before_request
def require_login():
    if request.endpoint in (None, "static", "login"):
        return
    if "user" not in session:
        return redirect(url_for("login"))


def db_error(e):
    msg = e.msg
    if e.errno == 1062:
        msg = "Duplicate entry - that value already exists."
    elif e.errno in (1451, 1452):
        msg = "Operation blocked: related records exist (or are missing)."
    flash(msg, "error")


# ------------------------------------------------------------------- auth
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        u = run("SELECT * FROM users WHERE username=%s",
                (request.form["username"].strip(),), "one")
        if u and check_password_hash(u["password_hash"], request.form["password"]):
            session["user"] = u["username"]
            return redirect(url_for("dashboard"))
        flash("Invalid username or password.", "error")
    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


# -------------------------------------------------------------- dashboard
@app.route("/")
def dashboard():
    run("UPDATE policies SET status='Expired' WHERE status='Active' AND end_date < CURDATE()")
    stats = run("""SELECT
        (SELECT COUNT(*) FROM customers) AS customers,
        (SELECT COUNT(*) FROM policies WHERE status='Active') AS active_policies,
        (SELECT COUNT(*) FROM claims WHERE status='Pending') AS pending_claims,
        (SELECT COALESCE(SUM(amount),0) FROM payments) AS revenue,
        (SELECT COALESCE(SUM(claim_amount),0) FROM claims WHERE status='Approved') AS payouts""",
        fetch="one")
    by_cat = run("""SELECT pl.category AS label, COUNT(*) AS n FROM policies po
                    JOIN plans pl ON pl.id = po.plan_id GROUP BY pl.category""", fetch="all")
    by_status = run("SELECT status AS label, COUNT(*) AS n FROM claims GROUP BY status", fetch="all")
    expiring = run("""SELECT po.*, c.full_name, pl.name AS plan_name FROM policies po
                      JOIN customers c ON c.id = po.customer_id
                      JOIN plans pl ON pl.id = po.plan_id
                      WHERE po.status='Active' AND po.end_date <= DATE_ADD(CURDATE(), INTERVAL 30 DAY)
                      ORDER BY po.end_date""", fetch="all")
    return render_template("dashboard.html", stats=stats, by_cat=by_cat,
                           by_status=by_status, expiring=expiring)


# -------------------------------------------------------------- customers
@app.route("/customers")
def customers():
    q = request.args.get("q", "").strip()
    sql = """SELECT c.*, (SELECT COUNT(*) FROM policies p WHERE p.customer_id=c.id) AS policy_count
             FROM customers c"""
    params = ()
    if q:
        sql += " WHERE c.full_name LIKE %s OR c.email LIKE %s OR c.phone LIKE %s"
        params = (f"%{q}%",) * 3
    rows = run(sql + " ORDER BY c.id DESC", params, "all")
    return render_template("customers.html", rows=rows, q=q)


@app.route("/customers/new", methods=["GET", "POST"])
@app.route("/customers/<int:cid>/edit", methods=["GET", "POST"])
def customer_form(cid=None):
    cust = run("SELECT * FROM customers WHERE id=%s", (cid,), "one") if cid else None
    if cid and not cust:
        abort(404)
    if request.method == "POST":
        f = request.form
        vals = (f["full_name"], f["email"], f["phone"], f["dob"] or None, f["address"] or None)
        try:
            if cid:
                run("""UPDATE customers SET full_name=%s, email=%s, phone=%s, dob=%s, address=%s
                       WHERE id=%s""", vals + (cid,))
                flash("Customer updated.", "success")
            else:
                run("""INSERT INTO customers (full_name, email, phone, dob, address)
                       VALUES (%s,%s,%s,%s,%s)""", vals)
                flash("Customer added.", "success")
            return redirect(url_for("customers"))
        except Error as e:
            db_error(e)
    return render_template("customer_form.html", c=cust)


@app.route("/customers/<int:cid>/delete", methods=["POST"])
def customer_delete(cid):
    run("DELETE FROM customers WHERE id=%s", (cid,))
    flash("Customer and their policies deleted.", "success")
    return redirect(url_for("customers"))


# ------------------------------------------------------------------ plans
@app.route("/plans", methods=["GET", "POST"])
def plans():
    if request.method == "POST":
        f = request.form
        try:
            run("""INSERT INTO plans (name, category, coverage_amount, annual_premium, term_years, description)
                   VALUES (%s,%s,%s,%s,%s,%s)""",
                (f["name"], f["category"], f["coverage_amount"], f["annual_premium"],
                 f["term_years"], f["description"] or None))
            flash("Plan added.", "success")
        except Error as e:
            db_error(e)
        return redirect(url_for("plans"))
    rows = run("""SELECT pl.*, (SELECT COUNT(*) FROM policies po WHERE po.plan_id=pl.id) AS policy_count
                  FROM plans pl ORDER BY pl.category, pl.name""", fetch="all")
    return render_template("plans.html", rows=rows)


@app.route("/plans/<int:pid>/delete", methods=["POST"])
def plan_delete(pid):
    try:
        run("DELETE FROM plans WHERE id=%s", (pid,))
        flash("Plan deleted.", "success")
    except Error as e:
        db_error(e)
    return redirect(url_for("plans"))


# --------------------------------------------------------------- policies
@app.route("/policies")
def policies():
    status = request.args.get("status", "")
    sql = """SELECT po.*, c.full_name, pl.name AS plan_name, pl.category
             FROM policies po JOIN customers c ON c.id = po.customer_id
             JOIN plans pl ON pl.id = po.plan_id"""
    params = ()
    if status:
        sql += " WHERE po.status=%s"
        params = (status,)
    rows = run(sql + " ORDER BY po.id DESC", params, "all")
    return render_template("policies.html", rows=rows, status=status)


@app.route("/policies/new", methods=["GET", "POST"])
def policy_new():
    custs = run("SELECT id, full_name, email FROM customers ORDER BY full_name", fetch="all")
    plans_ = run("SELECT * FROM plans ORDER BY category, name", fetch="all")
    if request.method == "POST":
        f = request.form
        plan = run("SELECT * FROM plans WHERE id=%s", (f["plan_id"],), "one")
        start = date.fromisoformat(f["start_date"])
        try:
            end = start.replace(year=start.year + plan["term_years"])
        except ValueError:  # 29 Feb
            end = start + timedelta(days=365 * plan["term_years"])
        for _ in range(5):
            no = f"POL{start:%y%m}{random.randint(10000, 99999)}"
            try:
                run("""INSERT INTO policies (policy_no, customer_id, plan_id, start_date, end_date, premium)
                       VALUES (%s,%s,%s,%s,%s,%s)""",
                    (no, f["customer_id"], plan["id"], start, end, plan["annual_premium"]))
                flash(f"Policy {no} issued.", "success")
                return redirect(url_for("policies"))
            except Error as e:
                if e.errno == 1062:
                    continue
                db_error(e)
                break
    return render_template("policy_form.html", custs=custs, plans=plans_, today=date.today())


@app.route("/policies/<int:pid>/cancel", methods=["POST"])
def policy_cancel(pid):
    run("UPDATE policies SET status='Cancelled' WHERE id=%s AND status='Active'", (pid,))
    flash("Policy cancelled.", "success")
    return redirect(url_for("policies"))


# ----------------------------------------------------------------- claims
@app.route("/claims")
def claims():
    status = request.args.get("status", "")
    sql = """SELECT cl.*, po.policy_no, c.full_name, pl.coverage_amount
             FROM claims cl JOIN policies po ON po.id = cl.policy_id
             JOIN customers c ON c.id = po.customer_id
             JOIN plans pl ON pl.id = po.plan_id"""
    params = ()
    if status:
        sql += " WHERE cl.status=%s"
        params = (status,)
    rows = run(sql + " ORDER BY cl.id DESC", params, "all")
    return render_template("claims.html", rows=rows, status=status)


@app.route("/claims/new", methods=["GET", "POST"])
def claim_new():
    pols = run("""SELECT po.id, po.policy_no, c.full_name, pl.name AS plan_name, pl.coverage_amount
                  FROM policies po JOIN customers c ON c.id = po.customer_id
                  JOIN plans pl ON pl.id = po.plan_id
                  WHERE po.status='Active' ORDER BY po.policy_no""", fetch="all")
    if request.method == "POST":
        f = request.form
        pol = next((p for p in pols if str(p["id"]) == f["policy_id"]), None)
        amount = float(f["claim_amount"])
        if not pol:
            flash("Select an active policy.", "error")
        elif amount <= 0 or amount > float(pol["coverage_amount"]):
            flash(f"Claim must be between 1 and the coverage limit ({money(pol['coverage_amount'])}).", "error")
        else:
            try:
                no = f"CLM-{random.randint(100000, 999999)}"
                run("""INSERT INTO claims (claim_no, policy_id, claim_amount, reason, filed_on)
                       VALUES (%s,%s,%s,%s,CURDATE())""", (no, pol["id"], amount, f["reason"]))
                flash(f"Claim {no} filed.", "success")
                return redirect(url_for("claims"))
            except Error as e:
                db_error(e)
    return render_template("claim_form.html", pols=pols)


@app.route("/claims/<int:cid>/<action>", methods=["POST"])
def claim_action(cid, action):
    if action not in ("approve", "reject"):
        abort(404)
    claim = run("""SELECT cl.*, pl.coverage_amount FROM claims cl
                   JOIN policies po ON po.id = cl.policy_id
                   JOIN plans pl ON pl.id = po.plan_id WHERE cl.id=%s""", (cid,), "one")
    if not claim:
        abort(404)
    if claim["status"] != "Pending":
        flash("This claim has already been processed.", "error")
        return redirect(url_for("claims"))
    if action == "approve":
        paid = run("""SELECT COALESCE(SUM(claim_amount),0) AS t FROM claims
                      WHERE policy_id=%s AND status='Approved'""", (claim["policy_id"],), "one")["t"]
        if paid + claim["claim_amount"] > claim["coverage_amount"]:
            flash("Cannot approve: total approved claims would exceed the policy coverage.", "error")
            return redirect(url_for("claims"))
    status = "Approved" if action == "approve" else "Rejected"
    run("UPDATE claims SET status=%s, remarks=%s WHERE id=%s",
        (status, request.form.get("remarks") or None, cid))
    flash(f"Claim {claim['claim_no']} {status.lower()}.", "success")
    return redirect(url_for("claims"))


# --------------------------------------------------------------- payments
@app.route("/payments")
def payments():
    rows = run("""SELECT pm.*, po.policy_no, c.full_name FROM payments pm
                  JOIN policies po ON po.id = pm.policy_id
                  JOIN customers c ON c.id = po.customer_id ORDER BY pm.id DESC""", fetch="all")
    total = sum(float(r["amount"]) for r in rows)
    return render_template("payments.html", rows=rows, total=total)


@app.route("/payments/new", methods=["GET", "POST"])
def payment_new():
    pols = run("""SELECT po.id, po.policy_no, po.premium, c.full_name FROM policies po
                  JOIN customers c ON c.id = po.customer_id
                  WHERE po.status='Active' ORDER BY po.policy_no""", fetch="all")
    if request.method == "POST":
        f = request.form
        try:
            run("""INSERT INTO payments (reference, policy_id, amount, paid_on, method)
                   VALUES (%s,%s,%s,CURDATE(),%s)""",
                (f"PAY-{random.randint(100000, 999999)}", f["policy_id"], f["amount"], f["method"]))
            flash("Payment recorded.", "success")
            return redirect(url_for("payments"))
        except Error as e:
            db_error(e)
    return render_template("payment_form.html", pols=pols)


# ------------------------------------------------------------------ start
def init_admin():
    if not run("SELECT id FROM users LIMIT 1", fetch="one"):
        run("INSERT INTO users (username, password_hash) VALUES (%s,%s)",
            ("admin", generate_password_hash("admin123")))
        print("Default admin created -> username: admin / password: admin123")


if __name__ == "__main__":
    try:
        init_admin()
        print("Connected to MySQL successfully")
    except Error as e:
        print("MySQL connection failed:", e)
        print("Check config.py and make sure you ran schema.sql in Workbench.")
    app.run(debug=False, use_reloader=False)