from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters, CallbackQueryHandler

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
        "🔥 MEGA DOWNLOADER BOT",
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


    if text == "🎵 Qo‘shiq qidirish":

        context.user_data["search"] = True

        await update.message.reply_text(
            "Qo‘shiq nomini yozing"
        )
        return


    if context.user_data.get("search"):

        results = search_song(text)

        if not results:

            await update.message.reply_text("Topilmadi")
            return


        buttons = []

        for r in results:

            buttons.append([
                InlineKeyboardButton(
                    r["title"],
                    callback_data=r["url"]
                )
            ])

        await update.message.reply_text(
            "Natijalar:",
            reply_markup=InlineKeyboardMarkup(buttons)
        )

        context.user_data["search"] = False

        return


    if "http" in text:

        await update.message.reply_text("Video yuklanmoqda...")

        video = download_video(text)

        await update.message.reply_video(video=open(video,"rb"))


async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    url = query.data

    await query.message.reply_text("Qo‘shiq yuklanmoqda...")

    audio = download_audio(url)

    await query.message.reply_audio(audio=open(audio,"rb"))


app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message))
app.add_handler(CallbackQueryHandler(button))

print("MEGA BOT ISHLADI")

app.run_polling(drop_pending_updates=True)
