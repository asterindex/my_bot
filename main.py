from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
import os

# Твій Telegram ID — щоб бот знав, кому пересилати
# ADMIN_ID = 425850962 # ak
ADMIN_ID = 523219178
BOT_TOKEN = "7788026172:AAFzVua5v229CtrbrQQQX8YEtg-vDi4h93I"
# int(os.getenv("asterindex"))

# Словник: message_id адміністратора → user_id користувача
message_map = {}

async def handle_user_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    msg = update.message.text

    # Надсилаємо адміну повідомлення користувача
    sent = await context.bot.send_message(
        chat_id=ADMIN_ID,
        text=f"Користувач {user.first_name} ({user.id}) пише:\n\n{msg}"
    )

    # Запам'ятовуємо, хто це був
    message_map[sent.message_id] = user.id

async def handle_admin_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Перевіряємо, чи це відповідь на повідомлення
    if not update.message.reply_to_message:
        await update.message.reply_text("❗ Відповідай саме на повідомлення користувача.")
        return

    replied_id = update.message.reply_to_message.message_id
    reply_text = update.message.text

    # Шукаємо, кому потрібно надіслати відповідь
    user_id = message_map.get(replied_id)
    if user_id:
        await context.bot.send_message(chat_id=user_id, text=reply_text)
    else:
        await update.message.reply_text("❗ Не вдалося знайти користувача для відповіді.")

# Запуск бота
if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(MessageHandler(filters.TEXT & (~filters.REPLY), handle_user_message))
    app.add_handler(MessageHandler(filters.TEXT & filters.REPLY, handle_admin_reply))

    app.run_polling()