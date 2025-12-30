# bot_invite.py
from flask import Flask
from threading import Thread
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, ChatJoinRequestHandler, ContextTypes

# --- Read BOT_TOKEN from Render environment variable ---
BOT_TOKEN = os.environ["BOT_TOKEN"]

# --- Keep-alive Flask server ---
keep_alive = Flask("")

@keep_alive.route("/")
def home():
    return "Bot is alive!"

def run():
    keep_alive.run(host="0.0.0.0", port=8080)

Thread(target=run).start()

# --- Telegram bot ---
OTHER_CHANNELS_TEXT = """
👋 Welcome!

We also have other useful channels 👇

📊 Channel 1: https://t.me/+CgkHK4DHxr5mNjNi  

Join and stay updated 🔥
"""

async def handle_join_request(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.chat_join_request.from_user
    try:
        await context.bot.send_message(
            chat_id=user.id,
            text=OTHER_CHANNELS_TEXT
        )
    except Exception as e:
        print(f"Failed to message {user.id}: {e}")

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(ChatJoinRequestHandler(handle_join_request))

print("Bot is starting...")
app.run_polling()


