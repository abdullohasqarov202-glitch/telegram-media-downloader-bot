import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, ContextTypes, filters
from downloader import download_video, download_audio


TOKEN = os.getenv("TOKEN")

user_links = {}


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        "👋 Salom!\n\n"
        "YouTube / TikTok / Instagram link yuboring."
    )


async def link_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):

    url = update.message.text

    if "http" not in url:

        await update.message.reply_text(
            "❌ Iltimos video link yuboring."
        )
        return

    user_links[update.message.chat_id] = url

    keyboard = [
        [
            InlineKeyboardButton("🎬 Video", callback_data="video"),
            InlineKeyboardButton("🎵 MP3", callback_data="mp3")
        ]
    ]

    await update.message.reply_text(
        "Format tanlang:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    url = user_links.get(query.message.chat_id)

    if query.data == "video":

        msg = await query.message.reply_text("📥 Yuklanmoqda...")

        file = download_video(url)

        await query.message.reply_video(open(file, "rb"))

        os.remove(file)

        await msg.delete()

    if query.data == "mp3":

        msg = await query.message.reply_text("🎵 Yuklanmoqda...")

        file = download_audio(url)

        await query.message.reply_audio(open(file, "rb"))

        os.remove(file)

        await msg.delete()


app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, link_handler))
app.add_handler(CallbackQueryHandler(button))

print("🔥 BOT ISHLADI")

app.run_polling()
