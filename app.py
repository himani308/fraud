# from flask import Flask, render_template, request, redirect,session,jsonify
# import pandas as pd
# import joblib
# import sqlite3
# import matplotlib.pyplot as plt
# import seaborn as sns
# import plotly.express as px
# import os
# from datetime import datetime
# # from werkzeug.security import generate_password_hash, check_password_hash


# app = Flask(__name__)
# app.secret_key = "mysecretkey123"
# model = joblib.load("fraud_model.pkl")
# @app.route("/")
# def dashboard():
#     if "user" not in session:
#         return redirect("/login")

#     conn = get_db()
#     cursor = conn.cursor()

#     # Total transactions
#     cursor.execute("SELECT COUNT(*) FROM transactions")
#     total = cursor.fetchone()[0]

#     # Risk counts
#     cursor.execute("SELECT risk_level, COUNT(*) FROM transactions GROUP BY risk_level")
#     risk_data = cursor.fetchall()

#     # Last 7 transactions (for chart)
#     cursor.execute("SELECT created_at, amount FROM transactions ORDER BY id DESC LIMIT 7")
#     chart_data = cursor.fetchall()

#     conn.close()

#     # Format data
#     risk_dict = {"LOW": 0, "MEDIUM": 0, "HIGH": 0}
#     for r in risk_data:
#         risk_dict[r[0]] = r[1]

#     dates = [row[0] for row in chart_data][::-1]
#     amounts = [row[1] for row in chart_data][::-1]

#     return render_template(
#         "dashboard.html",
#         user=session["user"],
#         total=total,
#         risk=risk_dict,
#         dates=dates,
#         amounts=amounts
#     )

# @app.route("/register")
# def register():
#     return render_template("register.html")
# @app.route("/login")
# def login():
#     return render_template("login.html")
# @app.route("/fraud")
# def fraud():
#     return render_template("fraud.html")


#     return render_template("register.html")

# def generate_seaborn_graphs():
#     import pandas as pd
#     import os

#     df = pd.read_csv("model_results.csv")

#     if not os.path.exists("static"):
#         os.makedirs("static")

#     paths = {}

    
#     plt.figure()
#     sns.barplot(x="Model", y="ROC_AUC", data=df)
#     plt.title("Model Comparison")
#     plt.xticks(rotation=20)

#     paths["bar"] = "static/bar.png"
#     plt.savefig(paths["bar"])
#     plt.close()

  
#     plt.figure()
#     sns.lineplot(x="Model", y="ROC_AUC", data=df, marker='o')
#     plt.title("Performance Trend")

#     paths["line"] = "static/line.png"
#     plt.savefig(paths["line"])
#     plt.close()

#     plt.figure()
#     sns.pointplot(x="ROC_AUC", y="Model", data=df)
#     plt.title("Model Ranking")

#     paths["point"] = "static/point.png"
#     plt.savefig(paths["point"])
#     plt.close()

    
#     plt.figure()
#     sns.boxplot(x="ROC_AUC", data=df)
#     plt.title("Score Distribution")

#     paths["box"] = "static/box.png"
#     plt.savefig(paths["box"])
#     plt.close()
#     xgb = df[df["Model"] == "XGBoost"]

#     if not xgb.empty:
#         metrics_df = pd.DataFrame({
#             "Metric": ["ROC_AUC", "Accuracy", "Precision"],
#             "Value": [
#                 xgb["ROC_AUC"].values[0],
#                 xgb["Accuracy"].values[0],
#                 xgb["Precision"].values[0]
#             ]
#         })

#         plt.figure()
#         sns.lineplot(x="Metric", y="Value", data=metrics_df, marker='o')

#         plt.title("XGBoost Performance (Line Graph)")
#         plt.ylim(0, 1)   

#         paths["xgb_metrics"] = "static/xgb_line.png"
#         plt.savefig(paths["xgb_metrics"])
#         plt.close()

#     plt.figure()

#     sns.lineplot(
#         x="Model",
#         y="ROC_AUC",
#         data=df,
#         marker='o'
#     )

#     plt.title("ROC-AUC Comparison Across Models")
#     plt.ylim(0, 1)   

#     paths["roc_line"] = "static/roc_line.png"
#     plt.savefig(paths["roc_line"])
#     plt.close()
#     return paths
# # @app.route("/about")
# # def about():
# #     with open("model_scores.json") as f:
# #         scores = json.load(f)

# #     names = list(scores.keys())
# #     values = list(scores.values())

# #     plt.figure(figsize=(8,5))
# #     sns.barplot(x=names, y=values)
# #     plt.title("Model Comparison (ROC-AUC)")
# #     plt.ylim(0.5, 1)

# #     # save image
# #     img_path = os.path.join("static", "model_graph.png")
# #     plt.savefig(img_path)
# #     plt.close()

# #     fig = px.bar(
# #         x=names,
# #         y=values,
# #         labels={'x': 'Model', 'y': 'ROC-AUC'},
# #         title="Interactive Model Comparison"
# #     )

# #     plotly_graph = fig.to_html(full_html=False)

# #     return render_template(
# #         "about.html",
# #         plotly_graph=plotly_graph
# #     )

# @app.route("/about")
# def about():
#     graphs = generate_seaborn_graphs()

#     import pandas as pd
#     df = pd.read_csv("model_results.csv")

#     best = df.loc[df["ROC_AUC"].idxmax()]

#     return render_template(
#         "about.html",
#         graphs=graphs,
#         best_model=best["Model"],
#         best_score=round(best["ROC_AUC"], 3)
#     )
# def init_db():
#     conn = sqlite3.connect("transactions.db")
#     cursor = conn.cursor()

#     cursor.execute("""
#         CREATE TABLE IF NOT EXISTS transactions (
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             name TEXT,
#             transfer_to TEXT,
#             mobile TEXT,
#             amount REAL,
#             balance REAL,
#             device TEXT,
#             location TEXT,
#             hour INTEGER,
#             frequency INTEGER,
#             biometric INTEGER,
#             fraud_probability REAL,
#             risk_level TEXT,
#             created_at TEXT
#         )
#     """)
#     cursor.execute("""
#     CREATE TABLE IF NOT EXISTS users (
#         id INTEGER PRIMARY KEY AUTOINCREMENT,
#         name TEXT,
#         email TEXT UNIQUE,
#         password TEXT
#     )
#     """)

#     conn.commit()
#     conn.close()
 
# init_db()
# def get_db():
#     return sqlite3.connect("transactions.db", timeout=10)

# @app.route("/predict", methods=["POST"])
# def predict():
#         # Form data
#         name = request.form.get("name")
#         transfer_to = request.form.get("transfer_to")
#         mobile = request.form.get("mobile")

#         amount = float(request.form.get("amount"))
#         balance = float(request.form.get("balance"))

#         # device = request.form.get("device_change")
#         device = "mobile"
#         location = request.form.get("location_change", "unknown")

#         hour = int(request.form.get("hour_change") or 0)
#         frequency = int(request.form.get("frequency") or 1)
#         # biometric = int(request.form.get("biometric"))

     
#         is_mobile = 1   
#         is_transfer = 1
#         is_night = 1 if hour < 6 else 0

#         device_change = int(request.form.get("device_change") or 0)
#         location_change = int(request.form.get("location_change") or 0)
#         biometric = int(request.form.get("biometric") or 0)
#         # is_night = 1 if hour < 6 else 0

#         data = pd.DataFrame([[
#             amount, balance, is_mobile, is_transfer,
#             hour, device_change, location_change,
#             frequency, is_night, biometric
#         ]], columns=[
#             'Transaction_Amount',
#             'Account_Balance',
#             'Is_Mobile',
#             'Is_Transfer',
#             'Transaction_Hour',
#             'Device_Change',
#             'Location_Change',
#             'Transaction_Frequency',
#             'Is_Night',
#             'Biometric_Verified'
#         ])

#         prob = model.predict_proba(data)[0][1]

#         # Risk logic
#         if prob > 0.7:
#             risk = "HIGH"
#             action = " Transaction Blocked!"
#         elif prob > 0.4:
#             risk = "MEDIUM"
#             action = " OTP Verification Required!"
#         else:
#             risk = "LOW"
#             action = "Transaction Approved!"


#         conn = get_db()
#         cursor = conn.cursor()

#         cursor.execute("""
#             INSERT INTO transactions 
#             (name, transfer_to, mobile, amount, balance, device, location, hour, frequency, biometric, fraud_probability, risk_level, created_at)
#             VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
#         """, (
#             name, transfer_to, mobile, amount, balance, device,
#             location, hour, frequency, biometric,
#             float(prob), risk, datetime.now()
#         ))

#         conn.commit()
#         conn.close()

#         return render_template("result.html",
#                                probability=round(prob, 3),
#                                risk=risk,
#                                action=action)

# @app.route("/registerprocess", methods=["POST"])
# def registerprocess():
#     name = request.form["name"]
#     email = request.form["email"]
#     password = request.form["password"]

#     conn = get_db()
#     cursor = conn.cursor()

#     cursor.execute(
#         "INSERT INTO users (name, email, password) VALUES (?, ?, ?)",
#         (name, email, password)
#     )

#     conn.commit()
#     conn.close()

#     return redirect("/login")

# @app.route("/loginprocess", methods=["POST"])
# def loginprocess():
#     email = request.form["email"]
#     password = request.form["password"]

#     conn = get_db()
#     cursor = conn.cursor()

#     cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
#     user = cursor.fetchone()

#     conn.close()

#     if user and user[3] == password:
#         session["user"] = user[1]
#         return redirect("/")   # dashboard
#     else:
#         return redirect("/login")


# # @app.route("/get-data")
# # def get_data():
# #     risk = request.args.get("risk")
# #     days = int(request.args.get("days"))

# #     conn = get_db()
# #     cursor = conn.cursor()

# #     # Base query
# #     query = "SELECT created_at, amount, risk_level FROM transactions WHERE 1=1"

# #     # Risk filter
# #     if risk != "ALL":
# #         query += " AND risk_level = ?"

# #     # Time filter (last X days)
# #     query += " AND date(created_at) >= date('now', ?)"

# #     if risk != "ALL":
# #         cursor.execute(query, (risk, f"-{days} day"))
# #     else:
# #         cursor.execute(query, (f"-{days} day",))

# #     data = cursor.fetchall()
# #     conn.close()

# #     dates = [row[0] for row in data]
# #     amounts = [row[1] for row in data]

# #     return jsonify({
# #         "dates": dates,
# #         "amounts": amounts
# #     })

# @app.route("/logout")
# def logout():
#     session.pop("user", None)  
#     return redirect("/login") 


# if __name__ == "__main__":
#     app.run(debug=True)











from flask import Flask, render_template, request, redirect, session
import pandas as pd
import joblib
import sqlite3
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import os
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "mysecretkey123"

# Load ML model
model = joblib.load("fraud_model.pkl")


def init_db():
    conn = sqlite3.connect("transactions.db")
    cursor = conn.cursor()

    # # Users table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS userss (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        email TEXT UNIQUE,
        password TEXT,
        balance REAL DEFAULT 1000
    )
""")
    # cursor.execute("ALTER TABLE transactions ADD COLUMN user_id INTEGER")
    # cursor.execute("ALTER TABLE userss ADD COLUMN status TEXT DEFAULT 'ACTIVE';")


    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            name TEXT,
            transfer_to TEXT,
            mobile TEXT,
            amount REAL,
            balance REAL,
            device TEXT,
            location TEXT,
            hour INTEGER,
            frequency INTEGER,
            biometric INTEGER,
            fraud_probability REAL,
            risk_level TEXT,
            created_at TEXT
        )
    """)

    conn.commit()
    conn.close()


def get_db():
    return sqlite3.connect("/tmp/transactions.db", timeout=10)


init_db()



@app.route("/")
def dashboard():
    if "user_id" not in session:
        return redirect("/login")

    user_id = session["user_id"]

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM transactions WHERE user_id = ?", (user_id,))
    total = cursor.fetchone()[0]

    cursor.execute("""
        SELECT risk_level, COUNT(*) 
        FROM transactions 
        WHERE user_id = ?
        GROUP BY risk_level
    """, (user_id,))
    risk_data = cursor.fetchall()

    cursor.execute("""
        SELECT created_at, amount 
        FROM transactions 
        WHERE user_id = ?
        ORDER BY id DESC LIMIT 7
    """, (user_id,))
    chart_data = cursor.fetchall()

    conn.close()

    risk_dict = {"LOW": 0, "MEDIUM": 0, "HIGH": 0}
    for r in risk_data:
        risk_dict[r[0]] = r[1]

    dates = [row[0] for row in chart_data][::-1]
    amounts = [row[1] for row in chart_data][::-1]

    return render_template(
        "dashboard.html",
        user=session["user"],
        total=total,
        risk=risk_dict,
        dates=dates,
        amounts=amounts
    )


@app.route("/login")
def login():
    return render_template("login.html")


@app.route("/register")
def register():
    return render_template("register.html")


@app.route("/fraud")
def fraud():
    if "user_id" not in session:
        return redirect("/login")
    return render_template("fraud.html")


@app.route("/registerprocess", methods=["POST"])
def registerprocess():
    name = request.form["name"]
    email = request.form["email"]
    password = generate_password_hash(request.form["password"])

    # ADD DEFAULT BALANCE
    balance =request.form["balance"] 

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO userss (name, email, password, balance) VALUES (?, ?, ?, ?)",
        (name, email, password, balance)
    )

    conn.commit()
    conn.close()

    return redirect("/login")


@app.route("/loginprocess", methods=["POST"])
def loginprocess():
    email = request.form["email"]
    password = request.form["password"]

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM userss WHERE email = ?", (email,))
    user = cursor.fetchone()

    conn.close()

    if user and check_password_hash(user[3], password):
        session["user"] = user[1]
        session["user_id"] = user[0]
        return redirect("/")
    else:
        return redirect("/login")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

@app.route("/aboutbitcoin")
def aboutbitcoin():
    return render_template("about.html")


@app.route("/predict", methods=["POST"])
def predict():
    if "user_id" not in session:
        return redirect("/login")

    user_id = session["user_id"]
    name = request.form.get("name")
    transfer_to = request.form.get("transfer_to")
    mobile = request.form.get("mobile")

    amount = float(request.form.get("amount"))
    balance = float(request.form.get("balance"))

    hour = int(request.form.get("hour_change") or 0)
    frequency = int(request.form.get("frequency") or 1)

    device_change = int(request.form.get("device_change") or 0)
    location_change = int(request.form.get("location_change") or 0)
    real_location = request.form.get("real_location")

    if location_change == 0:
        location = real_location
    else:
        location = "Changed Location"
    biometric = int(request.form.get("biometric") or 0)

    is_mobile = 1
    is_transfer = 1
    is_night = 1 if hour < 6 else 0

    data = pd.DataFrame([[
        amount, balance, is_mobile, is_transfer,
        hour, device_change, location_change,
        frequency, is_night, biometric
    ]], columns=[
        'Transaction_Amount',
        'Account_Balance',
        'Is_Mobile',
        'Is_Transfer',
        'Transaction_Hour',
        'Device_Change',
        'Location_Change',
        'Transaction_Frequency',
        'Is_Night',
        'Biometric_Verified'
    ])

    prob = model.predict_proba(data)[0][1]

    if prob > 0.7:
        risk = "HIGH"
        action = "Transaction Blocked!"
    elif prob > 0.4:
        risk = "MEDIUM"
        action = "OTP Verification Required!"
    else:
        risk = "LOW"
        action = "Transaction Approved!"

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO transactions 
        (user_id, name, transfer_to, mobile, amount, balance, device, location, hour, frequency, biometric, fraud_probability, risk_level, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        user_id, name, transfer_to, mobile, amount, balance,
        "mobile", "unknown", hour, frequency, biometric,
        float(prob), risk, datetime.now()
    ))

    conn.commit()
    conn.close()

    return render_template("result.html",
                           probability=round(prob, 3),
                           risk=risk,
                           action=action)

@app.route("/about")
def about():
    graphs = generate_seaborn_graphs()

    import pandas as pd
    df = pd.read_csv("model_results.csv")

    best = df.loc[df["ROC_AUC"].idxmax()]

    return render_template(
        "admin/about_a.html",
        graphs=graphs,
        best_model=best["Model"],
        best_score=round(best["ROC_AUC"], 3)
    )
def generate_seaborn_graphs():
    import pandas as pd
    import os

    df = pd.read_csv("model_results.csv")

    if not os.path.exists("static"):
        os.makedirs("static")

    paths = {}

    
    plt.figure()
    sns.barplot(x="Model", y="ROC_AUC", data=df)
    plt.title("Model Comparison")
    plt.xticks(rotation=20)

    paths["bar"] = "static/bar.png"
    plt.savefig(paths["bar"])
    plt.close()

  
    plt.figure()
    sns.lineplot(x="Model", y="ROC_AUC", data=df, marker='o')
    plt.title("Performance Trend")

    paths["line"] = "static/line.png"
    plt.savefig(paths["line"])
    plt.close()

    plt.figure()
    sns.pointplot(x="ROC_AUC", y="Model", data=df)
    plt.title("Model Ranking")

    paths["point"] = "static/point.png"
    plt.savefig(paths["point"])
    plt.close()

    
    plt.figure()
    sns.boxplot(x="ROC_AUC", data=df)
    plt.title("Score Distribution")

    paths["box"] = "static/box.png"
    plt.savefig(paths["box"])
    plt.close()
    xgb = df[df["Model"] == "XGBoost"]

    if not xgb.empty:
        metrics_df = pd.DataFrame({
            "Metric": ["ROC_AUC", "Accuracy", "Precision"],
            "Value": [
                xgb["ROC_AUC"].values[0],
                xgb["Accuracy"].values[0],
                xgb["Precision"].values[0]
            ]
        })

        plt.figure()
        sns.lineplot(x="Metric", y="Value", data=metrics_df, marker='o')

        plt.title("XGBoost Performance (Line Graph)")
        plt.ylim(0, 1)   

        paths["xgb_metrics"] = "static/xgb_line.png"
        plt.savefig(paths["xgb_metrics"])
        plt.close()

    plt.figure()

    sns.lineplot(
        x="Model",
        y="ROC_AUC",
        data=df,
        marker='o'
    )

    plt.title("ROC-AUC Comparison Across Models")
    plt.ylim(0, 1)   

    paths["roc_line"] = "static/roc_line.png"
    plt.savefig(paths["roc_line"])
    plt.close()
    return paths




def get_user_balance(user_id):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT balance FROM userss WHERE id=?", (user_id,))
    return cur.fetchone()[0]


def get_today_txn(user_id):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        SELECT COUNT(*) FROM transactions 
        WHERE user_id=? AND DATE(created_at)=DATE('now')
    """, (user_id,))
    return cur.fetchone()[0]

@app.route("/sell", methods=["POST"])
def sell():
    if "user_id" not in session:
        return redirect("/login")

    user_id = session["user_id"]
    user_name = session["user"]

    # FORM DATA
    amount = float(request.form["amount"])
    transfer_to = request.form.get("transfer_to")
    mobile = request.form.get("mobile", "N/A")

    # USER DATA
    balance = get_user_balance(user_id)
    remaining_balance = balance
    #  CHECK BALANCE
    if amount > balance:
        return render_template("result.html",
            risk="FAILED",
            action=" Insufficient Balance",
            probability=0,
            name=user_name,
            transfer_to=transfer_to,
            amount=amount,
            balance=balance,
            device_change=0,
            location_change=0,
            biometric=0
        )

    # AUTO DETECT
    hour = datetime.now().hour
    frequency = get_today_txn(user_id)

    device_change = int(request.form.get("device_change", 0))
    biometric = int(request.form.get("biometric", 0))

    # LOCATION DETECTION
    lat = request.form.get("latitude")
    lon = request.form.get("longitude")

    if lat and lon:
        location = f"{lat},{lon}"
        location_change = 0
    else:
        location = "Unknown"
        location_change = 1

    # AUTO FEATURES
    is_mobile = 1
    is_transfer = 1
    is_night = 1 if hour < 6 else 0

    # MODEL INPUT
    data = pd.DataFrame([[ 
        amount, balance, is_mobile, is_transfer,
        hour, device_change, location_change,
        frequency, is_night, biometric
    ]], columns=[
        'Transaction_Amount',
        'Account_Balance',
        'Is_Mobile',
        'Is_Transfer',
        'Transaction_Hour',
        'Device_Change',
        'Location_Change',
        'Transaction_Frequency',
        'Is_Night',
        'Biometric_Verified'
    ])

    prob = model.predict_proba(data)[0][1]

    #  DECISION ENGINE
    if prob > 0.7:
        risk = "HIGH"
        action = " Fraud Detected! Transaction Blocked"

    elif prob > 0.4:
        risk = "MEDIUM"
        action = " OTP Verification Required"

    else:
        risk = "LOW"
        action = " Transaction Successful"

        # UPDATE BALANCE  FIXED TABLE NAME
        conn = get_db()
        cur = conn.cursor()
        cur.execute(
            "UPDATE userss SET balance = balance - ? WHERE id=?",
            (amount, user_id)
        )
        conn.commit()
        conn.close()
        # CALCULATE REMAINING BALANCE
        if risk == "LOW":
            remaining_balance = balance - amount
        else:
            remaining_balance = balance   

    # SAVE TRANSACTION
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO transactions 
        (user_id, name, transfer_to, mobile, amount, balance, device, location, hour, frequency, biometric, fraud_probability, risk_level, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        user_id,
        user_name,
        transfer_to,
        mobile,
        amount,
        balance,
        "mobile" if device_change == 0 else "new_device",
        location,
        hour,
        frequency,
        biometric,
        float(prob),
        risk,
        datetime.now()
    ))

    conn.commit()
    conn.close()

    # FINAL RESPONSE
    return render_template(
        "result.html",
        probability=round(prob, 3),
        risk=risk,
        action=action,
        name=user_name,
        transfer_to=transfer_to,
        amount=amount,
        balance=balance,
        device_change=device_change,
        location_change=location_change,
        remaining_balance=remaining_balance,
        biometric=biometric
    )


# ================= ADMIN DASHBOARD =================
@app.route("/admin")
def admin_dashboard():
    conn = get_db()
    cur = conn.cursor()

    # TOTAL USERS
    cur.execute("SELECT COUNT(*) FROM userss")
    total_users = cur.fetchone()[0]

    # TOTAL TRANSACTIONS
    cur.execute("SELECT COUNT(*) FROM transactions")
    total_txn = cur.fetchone()[0]

    # RISK COUNTS
    cur.execute("SELECT risk_level, COUNT(*) FROM transactions GROUP BY risk_level")
    risk_data = dict(cur.fetchall())

    high = risk_data.get("HIGH", 0)
    medium = risk_data.get("MEDIUM", 0)
    low = risk_data.get("LOW", 0)

    # LAST 7 DAYS DATA
    cur.execute("""
        SELECT DATE(created_at), COUNT(*) 
        FROM transactions 
        GROUP BY DATE(created_at)
        ORDER BY DATE(created_at) DESC LIMIT 7
    """)
    chart_data = cur.fetchall()

    conn.close()

    return render_template("/admin/a_dashboard.html",
        total_users=total_users,
        total_txn=total_txn,
        high=high,
        medium=medium,
        low=low,
        chart_data=chart_data
    )


@app.route("/admin/users")
def manage_users():
    conn = get_db()
    cur = conn.cursor()

    cur.execute("SELECT id, name, email, balance,status FROM userss")
    users = cur.fetchall()

    conn.close()

    return render_template("/admin/admin_user.html", users=users)

@app.route("/admin/toggle_user/<int:user_id>")
def toggle_user(user_id):
    conn = get_db()
    cur = conn.cursor()

    # Get current status
    cur.execute("SELECT status FROM userss WHERE id=?", (user_id,))
    status = cur.fetchone()[0]

    # Toggle
    new_status = "BLOCKED" if status == "ACTIVE" else "ACTIVE"

    cur.execute("UPDATE userss SET status=? WHERE id=?", (new_status, user_id))
    conn.commit()
    conn.close()

    return redirect("/admin/users")

@app.route("/admin/user/<int:user_id>")
def view_user_transactions(user_id):
    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
        SELECT name, transfer_to, amount, risk_level, created_at 
        FROM transactions 
        WHERE user_id=?
        ORDER BY created_at DESC
    """, (user_id,))

    transactions = cur.fetchall()
    conn.close()

    return render_template("/admin/user_transcation.html", transactions=transactions)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

# if __name__ == "__main__":
    # app.run(debug=True)
    # app.run(debug=True, host="10.29.211.9", port=5000)
    













# from flask import Flask, render_template, request, redirect, session
# import pandas as pd
# import joblib
# import sqlite3
# import matplotlib.pyplot as plt
# import seaborn as sns
# import os
# from datetime import datetime
# from werkzeug.security import generate_password_hash, check_password_hash

# app = Flask(__name__)
# app.secret_key = "mysecretkey123"

# # Load ML model
# model = joblib.load("fraud_model.pkl")


# # ---------------- DATABASE ---------------- #
# def get_db():
#     return sqlite3.connect("transactions.db", timeout=10)


# def init_db():
#     conn = get_db()
#     cursor = conn.cursor()

#     cursor.execute("""
#     CREATE TABLE IF NOT EXISTS users (
#         id INTEGER PRIMARY KEY AUTOINCREMENT,
#         name TEXT,
#         email TEXT UNIQUE,
#         password TEXT,
#         balance REAL DEFAULT 1000
#     )
#     """)

#     cursor.execute("""
#     CREATE TABLE IF NOT EXISTS transactions (
#         id INTEGER PRIMARY KEY AUTOINCREMENT,
#         user_id INTEGER,
#         name TEXT,
#         transfer_to TEXT,
#         mobile TEXT,
#         amount REAL,
#         balance REAL,
#         device TEXT,
#         location TEXT,
#         hour INTEGER,
#         frequency INTEGER,
#         biometric INTEGER,
#         fraud_probability REAL,
#         risk_level TEXT,
#         created_at TEXT
#     )
#     """)

#     conn.commit()
#     conn.close()


# init_db()


# # ---------------- DASHBOARD ---------------- #
# @app.route("/")
# def dashboard():
#     if "user_id" not in session:
#         return redirect("/login")

#     user_id = session["user_id"]

#     conn = get_db()
#     cursor = conn.cursor()

#     cursor.execute("SELECT COUNT(*) FROM transactions WHERE user_id=?", (user_id,))
#     total = cursor.fetchone()[0]

#     cursor.execute("""
#         SELECT risk_level, COUNT(*) 
#         FROM transactions 
#         WHERE user_id=?
#         GROUP BY risk_level
#     """, (user_id,))
#     risk_data = cursor.fetchall()

#     cursor.execute("""
#         SELECT created_at, amount 
#         FROM transactions 
#         WHERE user_id=?
#         ORDER BY id DESC LIMIT 7
#     """, (user_id,))
#     chart_data = cursor.fetchall()

#     conn.close()

#     risk_dict = {"LOW": 0, "MEDIUM": 0, "HIGH": 0}
#     for r in risk_data:
#         risk_dict[r[0]] = r[1]

#     dates = [row[0] for row in chart_data][::-1]
#     amounts = [row[1] for row in chart_data][::-1]

#     return render_template(
#         "dashboard.html",
#         user=session["user"],
#         total=total,
#         risk=risk_dict,
#         dates=dates,
#         amounts=amounts
#     )


# # ---------------- AUTH ---------------- #
# @app.route("/login")
# def login():
#     return render_template("login.html")


# @app.route("/register")
# def register():
#     return render_template("register.html")


# @app.route("/logout")
# def logout():
#     session.clear()
#     return redirect("/login")


# @app.route("/registerprocess", methods=["POST"])
# def registerprocess():
#     name = request.form["name"]
#     email = request.form["email"]
#     password = generate_password_hash(request.form["password"])

#     conn = get_db()
#     cursor = conn.cursor()

#     cursor.execute(
#         "INSERT INTO users (name, email, password) VALUES (?, ?, ?)",
#         (name, email, password)
#     )

#     conn.commit()
#     conn.close()

#     return redirect("/login")


# @app.route("/loginprocess", methods=["POST"])
# def loginprocess():
#     email = request.form["email"]
#     password = request.form["password"]

#     conn = get_db()
#     cursor = conn.cursor()

#     cursor.execute("SELECT * FROM users WHERE email=?", (email,))
#     user = cursor.fetchone()

#     conn.close()

#     if user and check_password_hash(user[3], password):
#         session["user"] = user[1]
#         session["user_id"] = user[0]
#         return redirect("/")
#     else:
#         return redirect("/login")


# # ---------------- FRAUD PAGE ---------------- #
# @app.route("/fraud")
# def fraud():
#     if "user_id" not in session:
#         return redirect("/login")
#     return render_template("fraud.html")


# # ---------------- PREDICTION ---------------- #
# @app.route("/predict", methods=["POST"])
# def predict():
#     if "user_id" not in session:
#         return redirect("/login")

#     user_id = session["user_id"]

#     name = request.form.get("name")
#     transfer_to = request.form.get("transfer_to")
#     mobile = request.form.get("mobile")

#     amount = float(request.form.get("amount"))
#     balance = float(request.form.get("balance"))

#     hour = int(request.form.get("hour_change") or 0)
#     frequency = int(request.form.get("frequency") or 1)

#     device_change = int(request.form.get("device_change") or 0)
#     location_change = int(request.form.get("location_change") or 0)
#     biometric = int(request.form.get("biometric") or 0)

#     location = "Changed" if location_change == 1 else "Normal"
#     device = "New Device" if device_change == 1 else "Same Device"

#     is_mobile = 1
#     is_transfer = 1
#     is_night = 1 if hour < 6 else 0

#     data = pd.DataFrame([[
#         amount, balance, is_mobile, is_transfer,
#         hour, device_change, location_change,
#         frequency, is_night, biometric
#     ]], columns=[
#         'Transaction_Amount',
#         'Account_Balance',
#         'Is_Mobile',
#         'Is_Transfer',
#         'Transaction_Hour',
#         'Device_Change',
#         'Location_Change',
#         'Transaction_Frequency',
#         'Is_Night',
#         'Biometric_Verified'
#     ])

#     prob = model.predict_proba(data)[0][1]

#     # Risk logic
#     if prob > 0.7:
#         risk = "HIGH"
#         action = "Transaction Blocked!"
#     elif prob > 0.4:
#         risk = "MEDIUM"
#         action = "OTP Verification Required!"
#     else:
#         risk = "LOW"
#         action = "Transaction Approved!"

#         # Deduct balance ONLY if safe
#         conn = get_db()
#         cursor = conn.cursor()
#         cursor.execute(
#             "UPDATE users SET balance = balance - ? WHERE id=?",
#             (amount, user_id)
#         )
#         conn.commit()
#         conn.close()

#     # Save transaction
#     conn = get_db()
#     cursor = conn.cursor()

#     cursor.execute("""
#         INSERT INTO transactions 
#         (user_id, name, transfer_to, mobile, amount, balance, device, location, hour, frequency, biometric, fraud_probability, risk_level, created_at)
#         VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
#     """, (
#         user_id, name, transfer_to, mobile, amount, balance,
#         device, location, hour, frequency, biometric,
#         float(prob), risk, datetime.now()
#     ))

#     conn.commit()
#     conn.close()

#     return render_template("result.html",
#                            probability=round(prob, 3),
#                            risk=risk,
#                            action=action)


# # ---------------- ABOUT (MODEL COMPARISON) ---------------- #
# @app.route("/about")
# def about():
#     graphs = generate_graphs()

#     df = pd.read_csv("model_results.csv")
#     best = df.loc[df["ROC_AUC"].idxmax()]

#     return render_template(
#         "about.html",
#         graphs=graphs,
#         best_model=best["Model"],
#         best_score=round(best["ROC_AUC"], 3)
#     )
# @app.route("/sell", methods=["POST"])
# def sell():
#     if "user_id" not in session:
#         return redirect("/login")

#     user_id = session["user_id"]

#     amount = float(request.form["amount"])
#     device_change = int(request.form.get("device_change", 0))
#     location_change = int(request.form.get("location_change", 0))
#     biometric = int(request.form.get("biometric", 0))

#     # Get current balance
#     conn = get_db()
#     cursor = conn.cursor()
#     cursor.execute("SELECT balance FROM users WHERE id=?", (user_id,))
#     balance = cursor.fetchone()[0]

#     # Current hour
#     hour = datetime.now().hour

#     # Transaction frequency (today)
#     cursor.execute("""
#         SELECT COUNT(*) FROM transactions 
#         WHERE user_id=? AND DATE(created_at)=DATE('now')
#     """, (user_id,))
#     frequency = cursor.fetchone()[0]

#     is_mobile = 1
#     is_transfer = 1
#     is_night = 1 if hour < 6 else 0

#     # ML input
#     data = pd.DataFrame([[
#         amount, balance, is_mobile, is_transfer,
#         hour, device_change, location_change,
#         frequency, is_night, biometric
#     ]], columns=[
#         'Transaction_Amount',
#         'Account_Balance',
#         'Is_Mobile',
#         'Is_Transfer',
#         'Transaction_Hour',
#         'Device_Change',
#         'Location_Change',
#         'Transaction_Frequency',
#         'Is_Night',
#         'Biometric_Verified'
#     ])

#     prob = model.predict_proba(data)[0][1]

#     # Risk logic
#     if prob > 0.7:
#         risk = "HIGH"
#         message = "🚫 Fraud Detected! Transaction Blocked"
#     elif prob > 0.4:
#         risk = "MEDIUM"
#         message = "⚠️ OTP Verification Required"
#     else:
#         risk = "LOW"
#         message = "✅ Transaction Successful"

#         # Deduct balance
#         cursor.execute(
#             "UPDATE users SET balance = balance - ? WHERE id=?",
#             (amount, user_id)
#         )
#         conn.commit()

#     # Save transaction
#     cursor.execute("""
#         INSERT INTO transactions 
#         (user_id, amount, balance, device, location, hour, frequency, biometric, fraud_probability, risk_level, created_at)
#         VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
#     """, (
#         user_id, amount, balance,
#         "mobile", "unknown",
#         hour, frequency, biometric,
#         float(prob), risk, datetime.now()
#     ))

#     conn.commit()
#     conn.close()

#     return render_template("result.html", risk=risk, action=message)

# def generate_graphs():
#     df = pd.read_csv("model_results.csv")

#     if not os.path.exists("static"):
#         os.makedirs("static")

#     paths = {}

#     plt.figure()
#     sns.barplot(x="Model", y="ROC_AUC", data=df)
#     plt.xticks(rotation=20)
#     paths["bar"] = "static/bar.png"
#     plt.savefig(paths["bar"])
#     plt.close()

#     plt.figure()
#     sns.lineplot(x="Model", y="ROC_AUC", data=df, marker='o')
#     paths["line"] = "static/line.png"
#     plt.savefig(paths["line"])
#     plt.close()

#     plt.figure()
#     sns.boxplot(x="ROC_AUC", data=df)
#     paths["box"] = "static/box.png"
#     plt.savefig(paths["box"])
#     plt.close()

#     return paths


# # ---------------- RUN ---------------- #
# if __name__ == "__main__":
#     app.run(debug=True)