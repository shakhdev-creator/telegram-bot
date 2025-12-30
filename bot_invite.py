import os
import logging
import asyncio
from flask import Flask
from threading import Thread
from telegram import Update
from telegram.ext import ApplicationBuilder, ChatJoinRequestHandler, ContextTypes

# Logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Flask setup for Render's health check
server = Flask("")

@server.route("/")
def home():
    return "Bot is running!"

def run_flask():
    # Render provides the PORT environment variable automatically
    port = int(os.environ.get("PORT", 8080))
    server.run(host="0.0.0.0", port=port)

# --- Bot Logic ---
OTHER_CHANNELS_TEXT = """
👋 Welcome!

To join, check out our other useful channels 👇

📊 Channel 1: https://t.me/+CgkHK4DHxr5mNjNi  

Join and stay updated 🔥
"""

async def handle_join_request(update: Update, context: ContextTypes.DEFAULT_TYPE):
    request = update.chat_join_request
    user_id = request.from_user.id
    
    try:
        # 1. Send the private message
        await context.bot.send_message(chat_id=user_id, text=OTHER_CHANNELS_TEXT)
        # 2. Automatically approve the user
        await request.approve()
        logger.info(f"Approved user {user_id}")
    except Exception as e:
        logger.error(f"Error handling request: {e}")

# --- Main Execution ---
if __name__ == "__main__":
    # Start Flask in a separate thread
    Thread(target=run_flask).start()

    # Get Token from Render Environment Variables
    token = os.environ.get("BOT_TOKEN")
    
    if not token:
        logger.error("No BOT_TOKEN found in environment variables!")
    else:
        app = ApplicationBuilder().token(token).build()
        
        # Use ChatJoinRequestHandler for "Join Requests"
        app.add_handler(ChatJoinRequestHandler(handle_join_request))
        
        logger.info("Bot polling started...")
        app.run_polling()


