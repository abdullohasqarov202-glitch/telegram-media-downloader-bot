from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

from downloader import download_video, download_audio
from search import search_song
from config import TOKEN


menu = ReplyKeyboardMarkup(
[
["🎬 Video yuklash"],
["🎵 Qo‘shiq qidirish"],
["⬅️ Ortga"]
],
resize_keyboard=True
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        "🔥 ULTRA DOWNLOADER BOT",
        reply_markup=menu
    )


async def message(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = update.message.text


    if text == "⬅️ Ortga":

        await update.message.reply_text(
            "Bosh menyu",
            reply_markup=menu
        )
        return


    if text == "🎬 Video yuklash":

        await update.message.reply_text(
            "Link yuboring"
        )
        return


    if text == "🎵 Qo‘shiq qidirish":

        context.user_data["search"] = True

        await update.message.reply_text(
            "Qo‘shiq nomini yozing"
        )
        return


    if context.user_data.get("search"):

        url, title = search_song(text)

        await update.message.reply_text(
            f"Topildi: {title}\nYuklanmoqda..."
        )

        audio = download_audio(url)

        await update.message.reply_audio(audio=open(audio, "rb"))

        context.user_data["search"] = False

        return


    if "http" in text:

        await update.message.reply_text("Video yuklanmoqda...")

        video = download_video(text)

        await update.message.reply_video(video=open(video, "rb"))


app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message))

print("ULTRA BOT ISHLADI")

app.run_polling(drop_pending_updates=True)
