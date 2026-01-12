print("BOT FILE LOADED")
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import *
from db import orders, plans, accounts
from config import BOT_TOKEN, ADMIN_ID

def start(update: Update, context: CallbackContext):
    keyboard = []
    for p in plans.find():
        keyboard.append([InlineKeyboardButton(
            f"{p['name']} ₹{p['price']}",
            callback_data=f"plan_{p['_id']}"
        )])
    update.message.reply_text(
        "Welcome 🔑\nSelect a plan:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

def plan_select(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()

    order = {
        "user_id": query.from_user.id,
        "status": "pending"
    }
    oid = orders.insert_one(order).inserted_id

    query.message.reply_photo(
        photo=open("static/qr.png", "rb"),
        caption=f"""💳 Pay via UPI QR

Order ID: {oid}
After payment send:
UTR <space> OrderID"""
    )

def utr(update: Update, context: CallbackContext):
    try:
        utr_no, oid = update.message.text.split()
        orders.update_one(
            {"_id": oid},
            {"$set": {"utr": utr_no}}
        )
        update.message.reply_text("✅ UTR received. Wait for approval.")
    except:
        update.message.reply_text("❌ Format: UTR ORDERID")

def main():
    updater = Updater(BOT_TOKEN)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CallbackQueryHandler(plan_select, pattern="plan_"))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, utr))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
