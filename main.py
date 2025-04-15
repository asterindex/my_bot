from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
import os

# Твій Telegram ID — щоб бот знав, кому пересилати
# ADMIN_ID = 425850962 # ak
ADMIN_ID = int(os.getenv("ADMIN_ID", 0)) # 523219178
# BOT_TOKEN = "7619544899:AAHy0YELBPwqAAztN2j1BfJ7WU5Qzvwk2-0"
# BOT_TOKEN = "7788026172:AAFzVua5v229CtrbrQQQX8YEtg-vDi4h93I"
BOT_TOKEN = os.getenv("BOT_TOKEN")
# int(os.getenv("asterindex"))

# Зберігаємо відповідності: message_id => user_id
reply_map = {}

async def handle_user_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    msg = update.message.text
    print(msg)

    # Надсилаємо адміну повідомлення + зберігаємо кому відповісти
    sent = await context.bot.send_message(
        chat_id=ADMIN_ID,
        text=f"📩 Повідомлення від @{user.username or user.first_name} (ID {user.id}):\n\n{msg}"
    )
    reply_map[sent.message_id] = user.id  # запам'ятали, що це писав user.id

async def handle_admin_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Перевіряємо, чи це відповідь на повідомлення
    if not update.message.reply_to_message:
        await update.message.reply_text("❗ Відповідай на повідомлення користувача.")
        return

    replied_msg_id = update.message.reply_to_message.message_id
    target_user_id = reply_map.get(replied_msg_id)

    if not target_user_id:
        await update.message.reply_text("⚠️ Не вдалося знайти, кому відповісти.")
        return

    print(update.message.text)
    # Надсилаємо відповідь користувачу
    await context.bot.send_message(chat_id=target_user_id, text=update.message.text)

if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # повідомлення від користувачів (не адміна)
    app.add_handler(MessageHandler(filters.TEXT & (~filters.User(ADMIN_ID)) & ~filters.REPLY, handle_user_message))

    # відповіді адміна
    app.add_handler(MessageHandler(filters.TEXT & filters.User(ADMIN_ID) & filters.REPLY, handle_admin_reply))

    print("✅ Бот запущено")
    app.run_polling()