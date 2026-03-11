from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

from downloader import download_video, download_audio
from config import TOKEN, ADMIN_ID

users = set()

menu = ReplyKeyboardMarkup(
[
["🎬 Video yuklash"],
["🎵 MP3 yuklash"]
],
resize_keyboard=True
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    users.add(update.effective_user.id)

    await update.message.reply_text(
        "🤖 PRO DOWNLOADER BOT\n\nLink yuboring",
        reply_markup=menu
    )


async def admin(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if update.effective_user.id != ADMIN_ID:
        return

    await update.message.reply_text(
        f"👤 Foydalanuvchilar: {len(users)}"
    )


async def message(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = update.message.text


    if "youtube.com" in text or "youtu.be" in text:

        msg = await update.message.reply_text("⏳ Yuklanmoqda...")

        video = download_video(text)

        await update.message.reply_video(
            video=open(video, "rb")
        )

        audio = download_audio(text)

        await update.message.reply_audio(
            audio=open(audio, "rb")
        )

        await msg.delete()

        return


    if "instagram.com" in text or "tiktok.com" in text:

        msg = await update.message.reply_text("⏳ Yuklanmoqda...")

        video = download_video(text)

        await update.message.reply_video(
            video=open(video, "rb")
        )

        await msg.delete()

        return


app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("admin", admin))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message))

print("BOT ISHLADI")

app.run_polling()
