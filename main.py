from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
import os

# Твій Telegram ID — щоб бот знав, кому пересилати
ADMIN_ID = 425850962
# int(os.getenv("asterindex"))

# Зберігаємо відповідності між повідомленнями користувачів і твоїми відповідями
user_messages = {}

async def handle_user_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    msg = update.message.text

    # зберігаємо ID повідомлення для відповіді
    user_messages[user_id] = update.message

    # Пересилаємо повідомлення адміну (тобі)
    await context.bot.send_message(chat_id=ADMIN_ID, text=f"[{user_id}] питає:\n{msg}")

async def handle_admin_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    reply_to_text = update.message.text

    if not update.message.reply_to_message:
        await update.message.reply_text("Відповідай *на повідомлення користувача*!", parse_mode="Markdown")
        return

    # Витягаємо user_id з тексту оригінального повідомлення
    try:
        line = update.message.reply_to_message.text.split(']')[0]
        user_id = int(line.replace('[', ''))
    except:
        await update.message.reply_text("Не вдалося визначити користувача.")
        return

    await context.bot.send_message(chat_id=user_id, text=reply_to_text)

# Запуск
if __name__ == "__main__":
    import asyncio
    from dotenv import load_dotenv
    load_dotenv()

    # TOKEN = os.getenv("7619544899:AAHy0YELBPwqAAztN2j1BfJ7WU5Qzvwk2-0")
    TOKEN = "7619544899:AAHy0YELBPwqAAztN2j1BfJ7WU5Qzvwk2-0"

    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND) & (~filters.REPLY), handle_user_message))
    app.add_handler(MessageHandler(filters.TEXT & filters.REPLY, handle_admin_reply))

    print("Бот запущено...")
    app.run_polling()
