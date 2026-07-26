from telegram import (
    Update,
    ReplyKeyboardMarkup,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("📢 Kanal", url="https://t.me/Asqarov_2007"),
            InlineKeyboardButton("👨‍💻 Admin", url="https://t.me/Asqarov_0207"),
        ]
    ])

    text = f"""
<b>╔══════════════════════╗
🚀 PRO DOWNLOADER BOT
╚══════════════════════╝</b>

🎬 <b>YouTube</b>
📸 <b>Instagram</b>
🎵 <b>TikTok</b>
📘 <b>Facebook</b>

━━━━━━━━━━━━━━━━━━

✨ <b>Imkoniyatlar</b>

🎥 HD Video
🎵 MP3 Audio
⚡ Juda tez yuklash
🌍 100+ sayt qo'llab-quvvatlanadi

━━━━━━━━━━━━━━━━━━

👤 <b>Ism:</b> {update.effective_user.first_name}
🆔 <b>ID:</b> <code>{update.effective_user.id}</code>

👇 <b>Kerakli bo'limni tanlang.</b>
"""

    await update.message.reply_text(
        text,
        parse_mode="HTML",
        reply_markup=menu,
    )

    await update.message.reply_text(
        "💎 Premium xizmatlardan foydalanish uchun quyidagilardan birini tanlang:",
        reply_markup=keyboard,
    )
    msg = await update.message.reply_text("⏳ Yuklab olinmoqda...\n\n█░░░░░░░░░ 10%")
    await msg.edit_text("✅ Yuklab olindi!\n📤 Fayl yuborilmoqda...")
