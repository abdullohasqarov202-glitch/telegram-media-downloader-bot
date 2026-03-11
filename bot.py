from telegram import *
from telegram.ext import *

from downloader import download_video, download_audio
from search import search_song
from admin import add_user, get_users
from config import TOKEN, ADMIN

menu = ReplyKeyboardMarkup(
[
["🎬 Video yuklash"],
["🎵 Qo‘shiq qidirish"],
["📊 Statistika"]
],
resize_keyboard=True
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user = update.message.from_user

    add_user(user.id)

    await update.message.reply_text(
        "🔥 ULTRA PRO DOWNLOADER BOT",
        reply_markup=menu
    )


async def message(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = update.message.text
    user = update.message.from_user


    if text == "📊 Statistika":

        if user.username == ADMIN:

            users = get_users()

            await update.message.reply_text(
                f"👥 Users: {len(users)}"
            )

        return


    if text == "🎵 Qo‘shiq qidirish":

        context.user_data["search"] = True

        await update.message.reply_text("Qo‘shiq nomi yozing")

        return


    if context.user_data.get("search"):

        results = search_song(text)

        buttons = []

        for r in results:

            buttons.append(
                [InlineKeyboardButton(r["title"], callback_data=r["url"])]
            )

        await update.message.reply_text(
            "Natijalar:",
            reply_markup=InlineKeyboardMarkup(buttons)
        )

        context.user_data["search"] = False

        return


    if "http" in text:

        keyboard = InlineKeyboardMarkup([
        [
        InlineKeyboardButton("🎬 Video",callback_data=f"video|{text}"),
        InlineKeyboardButton("🎵 MP3",callback_data=f"audio|{text}")
        ]
        ])

        await update.message.reply_text(
            "Format tanlang",
            reply_markup=keyboard
        )


async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query

    await query.answer()

    data = query.data.split("|")

    action = data[0]
    url = data[1]


    if action == "video":

        await query.message.reply_text("Video yuklanmoqda...")

        file = download_video(url)

        await query.message.reply_video(open(file,"rb"))


    if action == "audio":

        await query.message.reply_text("MP3 yuklanmoqda...")

        file = download_audio(url)

        await query.message.reply_audio(open(file,"rb"))


app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message))
app.add_handler(CallbackQueryHandler(button))

print("ULTRA PRO BOT ISHLADI")

app.run_polling()
