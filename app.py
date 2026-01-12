from flask import Flask, render_template, request, redirect, session
from db import orders, accounts
from config import ADMIN_USER, ADMIN_PASS, ADMIN_ID
from telegram import Bot
from config import BOT_TOKEN

app = Flask(__name__)
app.secret_key = "secret"
bot = Bot(BOT_TOKEN)

@app.route("/", methods=["GET","POST"])
def login():
    if request.method == "POST":
        if request.form["user"] == ADMIN_USER and request.form["pass"] == ADMIN_PASS:
            session["admin"] = True
            return redirect("/dashboard")
    return render_template("login.html")

@app.route("/dashboard")
def dash():
    if not session.get("admin"):
        return redirect("/")
    return render_template("dashboard.html", orders=orders.find())

@app.route("/approve/<oid>")
def approve(oid):
    acc = accounts.find_one()
    orders.update_one({"_id": oid}, {"$set": {"status":"approved"}})
    accounts.delete_one({"_id": acc["_id"]})

    bot.send_message(
        chat_id=orders.find_one({"_id":oid})["user_id"],
        text=f"""✅ Payment Approved

Panel URL: {acc['url']}
Username: {acc['user']}
Password: {acc['pass']}"""
    )
    return redirect("/dashboard")

app.run(host="0.0.0.0", port=8080)
