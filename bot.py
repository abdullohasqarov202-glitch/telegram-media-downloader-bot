from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from downloader import download_video, download_audio
from config import TOKEN

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Salom 👋\n\n"
        "Link yuboring:\n"
        "YouTube / Instagram / TikTok\n\n"
        "🎬 Video yoki 🎵 MP3 yuklab beraman."
    )


async def handle_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text

    await update.message.reply_text("⏳ Yuklanmoqda...")

    file = download_video(url)

    if file:
        await update.message.reply_video(video=open(file, "rb"))
    else:
        await update.message.reply_text("❌ Yuklab bo‘lmadi")


async def mp3(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Link yozing: /mp3 link")
        return

    url = context.args[0]

    await update.message.reply_text("🎵 MP3 tayyorlanmoqda...")

    file = download_audio(url)

    if file:
        await update.message.reply_audio(audio=open(file, "rb"))
    else:
        await update.message.reply_text("❌ MP3 yuklab bo‘lmadi")


app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("mp3", mp3))
app.add_handler(MessageHandler(filters.TEXT, handle_link))

app.run_polling()
