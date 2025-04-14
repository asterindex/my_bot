from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("Сказати привіт", callback_data="hello")],
        [InlineKeyboardButton("Сказати час", callback_data="time")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Що хочеш зробити?", reply_markup=reply_markup)

# Обробка натискання кнопок
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "hello":
        await query.edit_message_text(text="Привіт, друже!")
    elif query.data == "time":
        from datetime import datetime
        now = datetime.now().strftime("%H:%M:%S")
        await query.edit_message_text(text=f"Зараз {now}")

# Ініціалізація бота
app = ApplicationBuilder().token("7619544899:AAHy0YELBPwqAAztN2j1BfJ7WU5Qzvwk2-0").build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button_handler))

app.run_polling()
