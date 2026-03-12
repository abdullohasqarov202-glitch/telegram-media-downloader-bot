import os
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

from downloader import download_video, download_audio

TOKEN = os.getenv("TOKEN")

menu = ReplyKeyboardMarkup(
    [["🎬 Video yuklash", "🎵 MP3 yuklash"]],
    resize_keyboard=True
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Salom!\n\n"
        "Link yuboring:\n"
        "YouTube / TikTok / Instagram",
        reply_markup=menu
    )

async def handle_link(update: Update, context: ContextTypes.DEFAULT_TYPE):

    url = update.message.text

    try:

        if "mp3" in url.lower():
            file = download_audio(url)

            with open(file, "rb") as f:
                await update.message.reply_audio(f)

        else:
            file = download_video(url)

            with open(file, "rb") as f:
                await update.message.reply_video(f)

    except:
        await update.message.reply_text("❌ Yuklab bo‘lmadi.")

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_link))

print("🚀 PRO DOWNLOADER BOT ISHLADI")

app.run_polling()
