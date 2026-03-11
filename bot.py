import yt_dlp
import uuid

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, ContextTypes, filters

TOKEN = "8761803905:AAFdKpuvFlMLsfVieetWbAs7MzIp0_5MUCM"
ADMIN_ID = 123456789

users = set()

# -------- MENU --------

def main_menu():

    keyboard = [
        [InlineKeyboardButton("🎵 Qo‘shiq qidirish", callback_data="music")],
        [InlineKeyboardButton("📥 Video yuklash", callback_data="video")]
    ]

    return InlineKeyboardMarkup(keyboard)


def back_menu():

    keyboard = [
        [InlineKeyboardButton("⬅️ Qaytish", callback_data="back")]
    ]

    return InlineKeyboardMarkup(keyboard)


# -------- SEARCH MUSIC --------

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

        for e in result["entries"]:

            songs.append({
                "title": e["title"],
                "url": e["webpage_url"]
            })

        return songs


# -------- DOWNLOAD AUDIO --------

def download_audio(url):

    filename = f"{uuid.uuid4().hex}.mp3"

    ydl_opts = {
        "format": "bestaudio",
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


# -------- DOWNLOAD VIDEO --------

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


# -------- START --------

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    users.add(update.effective_user.id)

    await update.message.reply_text(
        "🤖 VIDEO & MUSIC BOT\n\nBo‘limni tanlang 👇",
        reply_markup=main_menu()
    )


# -------- ADMIN --------

async def admin(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if update.effective_user.id != ADMIN_ID:
        return

    await update.message.reply_text(
        f"👑 ADMIN PANEL\n\n👤 Foydalanuvchilar: {len(users)}"
    )


# -------- BUTTON --------

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    if query.data == "music":

        context.user_data["mode"] = "music"

        await query.edit_message_text(
            "🎵 Qo‘shiq nomini yozing",
            reply_markup=back_menu()
        )


    elif query.data == "video":

        context.user_data["mode"] = "video"

        await query.edit_message_text(
            "📥 YouTube link yuboring",
            reply_markup=back_menu()
        )


    elif query.data == "back":

        context.user_data.clear()

        await query.edit_message_text(
            "🏠 Asosiy menyu",
            reply_markup=main_menu()
        )


    elif query.data.startswith("song_"):

        index = int(query.data.split("_")[1])

        songs = context.user_data["songs"]

        url = songs[index]["url"]

        await query.edit_message_text("⏳ MP3 yuklanmoqda...")

        audio = download_audio(url)

        await query.message.reply_audio(
            audio=open(audio, "rb")
        )


# -------- MESSAGE --------

async def message(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = update.message.text


    if context.user_data.get("mode") == "video":

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

        keyboard.append([InlineKeyboardButton("⬅️ Qaytish", callback_data="back")])

        await update.message.reply_text(
            "🎧 Topilgan qo‘shiqlar:",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )


# -------- RUN --------

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("admin", admin))
app.add_handler(CallbackQueryHandler(button))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message))

print("BOT ISHLADI")

app.run_polling()
