import os
import logging
from threading import Thread
from flask import Flask

from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)
from telegram.ext import (
    ApplicationBuilder,
    ChatJoinRequestHandler,
    ContextTypes
)

# ---------------- LOGGING ----------------
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ---------------- FLASK (Render health check) ----------------
server = Flask(__name__)

@server.route("/")
def home():
    return "Bot is running!"

def run_flask():
    port = int(os.environ.get("PORT", 8080))
    server.run(host="0.0.0.0", port=port)

# ---------------- BOT CONTENT ----------------

# ⚠️ VIP rasm URL (o‘zingiznikiga almashtiring)
VIP_IMAGE_URL = (
    "https://raw.githubusercontent.com/"
    "shakhdev-creator/telegram-bot/"
    "c90409f196f037449c6a26858ba887867de6108e/"
    "photo_2026-01-02_19-33-46.jpg"
)


VIP_TEXT = (
    "Assalomu alaykum va rahmatullohi va barakatuh 😊\n\n"
    "🎉 Tabriklaymiz! Siz 1000$ LIK VIP SIGNAL kanalini yutib oldingiz!\n\n"
    "🎯 VIP SIGNAL kanaliga qo‘shilish uchun "
    "“Qo‘shilish” tugmasini bosing 👇"
)

KEYBOARD = InlineKeyboardMarkup([
    [
        InlineKeyboardButton(
            "💎 1000$ lik kanal",
            url="https://t.me/+CgkHK4DHxr5mNjNi"
        )
    ],
    [
        InlineKeyboardButton(
            "➕ Qo‘shilish",
            url="https://t.me/+CgkHK4DHxr5mNjNi"
        )
    ]
])

# ---------------- JOIN REQUEST HANDLER ----------------
async def handle_join_request(update: Update, context: ContextTypes.DEFAULT_TYPE):
    request = update.chat_join_request
    user_id = request.from_user.id

    try:
        await context.bot.send_photo(
            chat_id=user_id,
            photo=VIP_IMAGE_URL,
            caption=VIP_TEXT,
            reply_markup=KEYBOARD
        )

        logger.info(f"VIP message sent to user {user_id}")

        # ❌ AGAR AUTO-APPROVE KERAK EMAS BO‘LSA — O‘CHIQ QOLADI
        # await request.approve()

    except Exception as e:
        logger.error(f"Error handling join request: {e}")

# ---------------- MAIN ----------------
if __name__ == "__main__":
    # Flask alohida thread’da ishlaydi
    Thread(target=run_flask).start()

    BOT_TOKEN = os.environ.get("BOT_TOKEN")

    if not BOT_TOKEN:
        logger.error("BOT_TOKEN not found in environment variables!")
    else:
        app = ApplicationBuilder().token(BOT_TOKEN).build()
        app.add_handler(ChatJoinRequestHandler(handle_join_request))

        logger.info("Bot polling started...")
        app.run_polling()


