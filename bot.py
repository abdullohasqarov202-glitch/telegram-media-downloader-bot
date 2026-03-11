import os

from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

from downloader import download_video, download_audio
from config import TOKEN, ADMIN_USERNAME


users_file = "users.txt"


def add_user(user_id):

    if not os.path.exists(users_file):
        open(users_file, "w").close()

    with open(users_file) as f:
        users = f.read().splitlines()

    if str(user_id) not in users:

        with open(users_file, "a") as f:
            f.write(str(user_id) + "\n")


def get_users():

    if not os.path.exists(users_file):
        return []

    with open(users_file) as f:
        return f.read().splitlines()


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    add_user(update.effective_user.id)

    await update.message.reply_text(
        "🔥 SUPER DOWNLOADER BOT\n\n"
        "Link yuboring:\n"
        "YouTube / Instagram / TikTok"
    )


async def admin(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if update.effective_user.username != ADMIN_USERNAME:
        return

    users = get_users()

    await update.message.reply_text(
        f"👑 ADMIN PANEL\n\nUsers: {len(users)}"
    )


async def broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if update.effective_user.username != ADMIN_USERNAME:
        return

    text = " ".join(context.args)

    users = get_users()

    for u in users:

        try:
            await context.bot.send_message(u, text)
        except:
            pass

    await update.message.reply_text("✅ Yuborildi")


async def message(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = update.message.text

    try:

        if "youtube.com" in text or "youtu.be" in text:

            msg = await update.message.reply_text("⏳ Video yuklanmoqda...")

            video = download_video(text)

            await update.message.reply_video(video=open(video, "rb"))

            audio = download_audio(text)

            await update.message.reply_audio(audio=open(audio, "rb"))

            await msg.delete()

            return


        if "instagram.com" in text or "tiktok.com" in text:

            msg = await update.message.reply_text("⏳ Video yuklanmoqda...")

            video = download_video(text)

            await update.message.reply_video(video=open(video, "rb"))

            await msg.delete()

    except Exception as e:

        await update.message.reply_text(
            "❌ Yuklab bo‘lmadi.\n"
            "Video private yoki bloklangan bo‘lishi mumkin."
        )


app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("admin", admin))
app.add_handler(CommandHandler("broadcast", broadcast))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message))

print("SUPER BOT ISHLADI")

app.run_polling(drop_pending_updates=True)
