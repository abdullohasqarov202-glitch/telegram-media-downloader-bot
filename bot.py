import os
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

from downloader import download_video, download_audio

TOKEN = os.getenv("TOKEN")

menu = ReplyKeyboardMarkup(
    [
        ["🎬 Video yuklash", "🎵 MP3 yuklash"],
        ["ℹ️ Yordam"]
    ],
    resize_keyboard=True,
)

# Foydalanuvchi tanlagan rejim
user_mode = {}


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "🚀 <b>PRO DOWNLOADER BOT</b>\n\n"
        "✅ YouTube\n"
        "✅ Instagram\n"
        "✅ TikTok\n\n"
        "Kerakli bo'limni tanlang 👇"
    )

    await update.message.reply_text(
        text,
        parse_mode="HTML",
        reply_markup=menu,
    )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = update.message.text

    # Tugmalar
    if text == "🎬 Video yuklash":
        user_mode[update.effective_user.id] = "video"
        await update.message.reply_text(
            "📎 Video havolasini yuboring."
        )
        return

    if text == "🎵 MP3 yuklash":
        user_mode[update.effective_user.id] = "audio"
        await update.message.reply_text(
            "🎵 Qo'shiq yoki video havolasini yuboring."
        )
        return

    if text == "ℹ️ Yordam":
        await update.message.reply_text(
            "Instagram, TikTok yoki YouTube linkini yuboring."
        )
        return

    # Link emas
    if not text.startswith(("http://", "https://")):
        await update.message.reply_text(
            "❌ Iltimos, havola yuboring."
        )
        return

    try:
        await update.message.reply_text("⏳ Yuklab olinmoqda...")

        mode = user_mode.get(update.effective_user.id, "video")

        if mode == "audio":
            file = download_audio(text)
            with open(file, "rb") as f:
                await update.message.reply_audio(f)
        else:
            file = download_video(text)
            with open(file, "rb") as f:
                await update.message.reply_video(f)

    except Exception as e:
        print(e)
        await update.message.reply_text(
            "❌ Yuklab bo'lmadi."
        )


app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

print("🚀 PRO DOWNLOADER BOT ISHLADI")

app.run_polling()
