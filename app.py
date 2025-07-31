from flask import Flask, render_template, request, redirect, session, url_for
from datetime import datetime, timedelta

app = Flask(__name__)
app.secret_key = 'meowsecret'

# Dummy-Datenbank
users = {
    "chafyyadmin1927291723928220": {
        "password": "yosupcookieilovemelon",
        "webmoney": 9999,
        "subscription": "year"
    }
}

@app.route("/")
def index():
    if "user" in session:
        user = users.get(session["user"])
        if user and user["subscription"]:
            return render_template("index.html", allowed=True)
    return render_template("index.html", allowed=False)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = request.form["username"]
        pw = request.form["password"]
        if user in users and users[user]["password"] == pw:
            session["user"] = user
            return redirect("/dashboard")
    return render_template("login.html")

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        user = request.form["username"]
        pw = request.form["password"]
        if user not in users:
            users[user] = {"password": pw, "webmoney": 0, "subscription": None}
            return redirect("/login")
    return render_template("signup.html")

@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect("/login")
    user = users[session["user"]]
    return render_template("dashboard.html", user=session["user"], money=user["webmoney"], subscription=user["subscription"])

@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect("/login")

if __name__ == "__main__":
    app.run()
