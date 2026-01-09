import os
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import (
    ApplicationBuilder,
    MessageHandler,
    CommandHandler,
    CallbackQueryHandler,
    filters,
    ContextTypes
)

BOT_TOKEN = os.getenv("BOT_TOKEN")

CHANNEL_ID = -1003559645064   # Channel
OWNER_ID = 8110146895            # Owner


# /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привет!\n"
        "Это бот для анонимных признаний.\n"
        "Напиши сообщение — и владелец решит публиковать его или нет ❤️\n"
	"Канал для сообщений\n"
	"https://t.me/Confessions_of_bot"
    )


async def forward(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not update.message or not update.message.text:
        return

    text = update.message.text

    await update.message.reply_text("Ваше признание отправлено на модерацию ✔")

    msg = (
        "💌 Новое анонимное признание на модерации:\n\n"
        f"{text}"
    )

    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("✔️ Опубликовать", callback_data=f"approve|{text}"),
                InlineKeyboardButton("❌ Отклонить", callback_data="reject")
            ]
        ]
    )

    await context.bot.send_message(
        chat_id=OWNER_ID,
        text=msg,
        reply_markup=keyboard
    )


async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    data = query.data

    if data == "reject":
        await query.edit_message_text("❌ Сообщение отклонено")
        return

    if data.startswith("approve|"):
        text = data.split("|", 1)[1]

        await context.bot.send_message(
            chat_id=CHANNEL_ID,
            text=f"💌 Анонимное признание:\n\n{text}"
        )

        await query.edit_message_text("✔️ Сообщение опубликовано")


app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, forward))
app.add_handler(CallbackQueryHandler(buttons))

app.run_polling()
