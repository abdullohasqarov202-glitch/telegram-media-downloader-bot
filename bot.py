import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from downloader import download_video, download_audio
from config import TOKEN, CHANNEL

users = set()

menu = ReplyKeyboardMarkup(
    [
        ["🎬 Video yuklash"],
        ["🎵 MP3 yuklash"]
    ],
    resize_keyboard=True
)


async def check_sub(user_id, bot):
    try:
        member = await bot.get_chat_member(CHANNEL, user_id)
        return member.status in ["member", "administrator", "creator"]
    except:
        return False


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user = update.effective_user.id
    users.add(user)

    if not await check_sub(user, context.bot):

        keyboard = [
            [InlineKeyboardButton("📢 Kanalga obuna", url=f"https://t.me/{CHANNEL.replace('@','')}")],
        ]

        await update.message.reply_text(
            "❗ Botdan foydalanish uchun kanalga obuna bo‘ling",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
        return

    await update.message.reply_text(
        "🤖 *Video Yuklab Ber Bot*\n\n"
        "📥 Link yuboring\n\n"
        "Platformalar:\n"
        "YouTube\n"
        "TikTok\n"
        "Instagram",
        parse_mode="Markdown",
        reply_markup=menu
    )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user = update.effective_user.id
    text = update.message.text

    if not await check_sub(user, context.bot):
        await update.message.reply_text("❌ Avval kanalga obuna bo‘ling")
        return

    if text.startswith("http"):

        msg = await update.message.reply_text("⏳ Yuklanmoqda...")

        video = download_video(text)

        if video:
            await update.message.reply_video(video=open(video, "rb"))
        else:
            await update.message.reply_text("❌ Video yuklanmadi")
            return

        audio = download_audio(text)

        if audio:
            await update.message.reply_audio(audio=open(audio, "rb"))

        await msg.delete()


async def mp3(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not context.args:
        await update.message.reply_text("❗ /mp3 link yozing")
        return

    url = context.args[0]

    msg = await update.message.reply_text("🎵 MP3 tayyorlanmoqda...")

    audio = download_audio(url)

    if audio:
        await update.message.reply_audio(audio=open(audio, "rb"))
    else:
        await update.message.reply_text("❌ MP3 yuklanmadi")

    await msg.delete()


async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"👥 Foydalanuvchilar: {len(users)}")


app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("mp3", mp3))
app.add_handler(CommandHandler("stats", stats))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

print("Bot ishga tushdi...")

app.run_polling()
