import yt_dlp
import uuid

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, ContextTypes, filters

TOKEN = "8761803905:AAFdKpuvFlMLsfVieetWbAs7MzIp0_5MUCM"


def search_music(query):

    ydl_opts = {
        "quiet": True,
        "skip_download": True
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:

        result = ydl.extract_info(
            f"ytsearch5:{query} music",
            download=False
        )

        songs = []

        for entry in result["entries"]:

            songs.append({
                "title": entry["title"],
                "url": entry["webpage_url"]
            })

        return songs



def download_audio(url):

    filename = f"{uuid.uuid4().hex}.mp3"

    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": filename,
        "quiet": True,
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192"
        }]
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    return filename



def download_video(url):

    filename = f"{uuid.uuid4().hex}.mp4"

    ydl_opts = {
        "format": "best",
        "outtmpl": filename,
        "quiet": True
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    return filename



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

        await query.edit_message_text("📥 YouTube link yuboring")


    elif query.data == "music":

        context.user_data["mode"] = "music"

        await query.edit_message_text("🎵 Qo‘shiq nomini yozing")


    elif query.data.startswith("song_"):

        index = int(query.data.split("_")[1])

        songs = context.user_data.get("songs")

        url = songs[index]["url"]

        await query.edit_message_text("⏳ MP3 yuklanmoqda...")

        audio = download_audio(url)

        await query.message.reply_audio(
            audio=open(audio, "rb")
        )



async def message(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = update.message.text


    if "http" in text:

        msg = await update.message.reply_text("⏳ Video yuklanmoqda...")

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


    if context.user_data.get("mode") == "music":

        songs = search_music(text)

        context.user_data["songs"] = songs

        keyboard = []

        for i, s in enumerate(songs):

            keyboard.append([
                InlineKeyboardButton(
                    s["title"][:40],
                    callback_data=f"song_{i}"
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

print("BOT ISHLADI")

app.run_polling()
