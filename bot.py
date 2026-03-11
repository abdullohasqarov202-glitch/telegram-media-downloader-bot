from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes
import yt_dlp

from downloader import download_video, download_audio
from config import TOKEN

CHANNEL = "@Asqarov_2007"


async def check_sub(user_id, bot):
    try:
        member = await bot.get_chat_member(CHANNEL, user_id)
        return member.status in ["member", "administrator", "creator"]
    except:
        return False


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user = update.effective_user.id

    if not await check_sub(user, context.bot):

        keyboard = [
            [InlineKeyboardButton("📢 Kanalga obuna bo'lish", url="https://t.me/Asqarov_2007")],
            [InlineKeyboardButton("✅ Tekshirish", callback_data="check")]
        ]

        await update.message.reply_text(
            "🚫 Botdan foydalanish uchun kanalga obuna bo‘ling",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
        return

    keyboard = [
        [
            InlineKeyboardButton("🎬 Video yuklash", callback_data="video"),
            InlineKeyboardButton("🎵 Qo‘shiq qidirish", callback_data="music")
        ]
    ]

    await update.message.reply_text(
        "🤖 Video Yuklab Ber Bot\n\n"
        "Quyidagidan birini tanlang 👇",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    if query.data == "check":

        if await check_sub(query.from_user.id, context.bot):

            keyboard = [
                [
                    InlineKeyboardButton("🎬 Video yuklash", callback_data="video"),
                    InlineKeyboardButton("🎵 Qo‘shiq qidirish", callback_data="music")
                ]
            ]

            await query.edit_message_text(
                "✅ Endi foydalanishingiz mumkin",
                reply_markup=InlineKeyboardMarkup(keyboard)
            )

        else:

            keyboard = [
                [InlineKeyboardButton("📢 Kanalga obuna bo'lish", url="https://t.me/Asqarov_2007")],
                [InlineKeyboardButton("🔄 Tekshirish", callback_data="check")]
            ]

            await query.edit_message_text(
                "❌ Avval kanalga obuna bo‘ling",
                reply_markup=InlineKeyboardMarkup(keyboard)
            )


    elif query.data == "video":

        context.user_data["mode"] = "video"

        await query.edit_message_text(
            "📥 Video link yuboring\n\n"
            "YouTube / TikTok / Instagram"
        )


    elif query.data == "music":

        context.user_data["mode"] = "music"

        await query.edit_message_text(
            "🎵 Qo‘shiq nomini yozing"
        )


    elif query.data.startswith("song_"):

        url = query.data.replace("song_", "")

        await query.edit_message_text("⏳ Yuklanmoqda...")

        audio = download_audio(url)

        if audio:
            await query.message.reply_audio(audio=open(audio, "rb"))
        else:
            await query.message.reply_text("❌ Yuklab bo‘lmadi")


def search_music(query):

    ydl_opts = {
        "quiet": True,
        "skip_download": True
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:

        result = ydl.extract_info(f"ytsearch5:{query}", download=False)

        songs = []

        for entry in result["entries"]:
            songs.append({
                "title": entry["title"],
                "url": entry["webpage_url"]
            })

        return songs


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = update.message.text
    mode = context.user_data.get("mode")


    if mode == "music":

        songs = search_music(text)

        keyboard = []

        for s in songs:

            keyboard.append([
                InlineKeyboardButton(
                    s["title"][:40],
                    callback_data=f"song_{s['url']}"
                )
            ])

        await update.message.reply_text(
            "🎧 Topilgan qo‘shiqlar:",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

        return


    if mode == "video":

        msg = await update.message.reply_text("⏳ Yuklanmoqda...")

        video = download_video(text)

        if video:
            await update.message.reply_video(video=open(video, "rb"))
        else:
            await update.message.reply_text("❌ Video yuklab bo‘lmadi")

        await msg.delete()


app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(buttons))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

print("Bot ishga tushdi...")

app.run_polling()
