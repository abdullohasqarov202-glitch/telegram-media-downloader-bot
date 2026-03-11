from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, ContextTypes, filters
import yt_dlp

from downloader import download_video, download_audio
from config import ABDULLOH


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    keyboard = [
        [
            InlineKeyboardButton("🎬 Video yuklash", callback_data="video"),
            InlineKeyboardButton("🎵 Qo‘shiq qidirish", callback_data="music")
        ]
    ]

    await update.message.reply_text(
        "🤖 VIDEO YUKLAB BER BOT\n\nBo‘limni tanlang 👇",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    if query.data == "video":

        context.user_data["mode"] = "video"

        await query.edit_message_text(
            "📥 Video link yuboring"
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

            await query.message.reply_audio(
                audio=open(audio, "rb")
            )


def search_music(query):

    ydl_opts = {
        "quiet": True,
        "skip_download": True
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:

        result = ydl.extract_info(
            f"ytsearch5:{query}",
            download=False
        )

        songs = []

        if "entries" in result:

            for entry in result["entries"]:

                songs.append({
                    "title": entry.get("title"),
                    "url": entry.get("webpage_url")
                })

        return songs


async def message(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = update.message.text


    # agar link tashlasa
    if "http" in text:

        msg = await update.message.reply_text("⏳ Yuklanmoqda...")

        video = download_video(text)

        if video:
            await update.message.reply_video(video=open(video, "rb"))

        audio = download_audio(text)

        if audio:
            await update.message.reply_audio(audio=open(audio, "rb"))

        await msg.delete()

        return


    mode = context.user_data.get("mode")


    if mode == "music":

        songs = search_music(text)

        if not songs:

            await update.message.reply_text("❌ Qo‘shiq topilmadi")
            return


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


app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message))

print("Bot ishga tushdi...")

app.run_polling()
