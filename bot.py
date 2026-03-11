from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes
from downloader import download_video, download_audio
from config import TOKEN

CHANNEL = "@Asqarov_2007"


# OBUNA TEKSHIRISH
async def check_sub(user_id, bot):
    try:
        member = await bot.get_chat_member(CHANNEL, user_id)
        return member.status in ["member", "administrator", "creator"]
    except:
        return False


# START
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user = update.effective_user.id
    bot = context.bot

    if not await check_sub(user, bot):

        keyboard = [
            [InlineKeyboardButton("📢 Kanalga obuna bo'lish", url="https://t.me/Asqarov_2007")],
            [InlineKeyboardButton("✅ Tekshirish", callback_data="check")]
        ]

        await update.message.reply_text(
            "🚫 *Botdan foydalanish uchun kanalga obuna bo‘ling!*\n\n"
            "👇 Pastdagi tugma orqali obuna bo‘ling",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
        return

    await update.message.reply_text(
        "🎬 *Video Yuklab Ber Bot*\n\n"
        "Quyidagi platformalardan yuklab beradi:\n\n"
        "▶️ YouTube\n"
        "📸 Instagram\n"
        "🎵 TikTok\n\n"
        "📥 *Link yuboring!*",
        parse_mode="Markdown"
    )


# TEKSHIRISH TUGMASI
async def check_button(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    user = query.from_user.id
    bot = context.bot

    await query.answer()

    if await check_sub(user, bot):

        await query.edit_message_text(
            "✅ *Rahmat! Siz kanalga obuna bo‘lgansiz*\n\n"
            "🤖 *Video Yuklab Ber Bot*\n\n"
            "📥 Endi menga video link yuboring!\n\n"
            "Qo‘llab-quvvatlanadi:\n"
            "▶️ YouTube\n"
            "📸 Instagram\n"
            "🎵 TikTok",
            parse_mode="Markdown"
        )

    else:

        keyboard = [
            [InlineKeyboardButton("📢 Kanalga obuna bo'lish", url="https://t.me/Asqarov_2007")],
            [InlineKeyboardButton("🔄 Qayta tekshirish", callback_data="check")]
        ]

        await query.edit_message_text(
            "❌ *Siz hali kanalga obuna bo‘lmagansiz!*\n\n"
            "👇 Obuna bo‘lib qayta tekshiring",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )


# LINK QABUL QILISH
async def handle_link(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user = update.effective_user.id
    bot = context.bot

    if not await check_sub(user, bot):
        await update.message.reply_text(
            "❌ Avval kanalga obuna bo‘ling:\n"
            "👉 https://t.me/Asqarov_2007"
        )
        return

    url = update.message.text

    msg = await update.message.reply_text("⏳ Yuklanmoqda...")

    video_file = download_video(url)

    if video_file:
        await update.message.reply_video(video=open(video_file, "rb"))
    else:
        await update.message.reply_text("❌ Video yuklab bo‘lmadi")
        return

    audio_file = download_audio(url)

    if audio_file:
        await update.message.reply_audio(audio=open(audio_file, "rb"))
    else:
        await update.message.reply_text("❌ MP3 yuklab bo‘lmadi")

    await msg.delete()


# MP3 COMMAND
async def mp3(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not context.args:
        await update.message.reply_text(
            "❗ Link yozing\n\n"
            "Misol:\n"
            "/mp3 https://youtube.com/..."
        )
        return

    url = context.args[0]

    await update.message.reply_text("🎵 MP3 tayyorlanmoqda...")

    audio_file = download_audio(url)

    if audio_file:
        await update.message.reply_audio(audio=open(audio_file, "rb"))
    else:
        await update.message.reply_text("❌ MP3 yuklab bo‘lmadi")


# APPLICATION
app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("mp3", mp3))
app.add_handler(CallbackQueryHandler(check_button))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_link))

print("Bot ishga tushdi...")

app.run_polling()
