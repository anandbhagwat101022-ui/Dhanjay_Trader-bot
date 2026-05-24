
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = "8639623533:AAFypjCIe5q2WIsTGe7Ws-P2eDVz3tAh2xY"

# Signal command
async def signal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        pair = context.args[0]
        direction = context.args[1]
        time = context.args[2]

        message = f"""
📊 TRADE SIGNAL

Pair: {pair}
Direction: {direction}
Time: {time}
"""
        await update.message.reply_text(message)

    except:
        await update.message.reply_text("❌ Use: /signal EURUSD CALL 1min")

# Result command
async def result(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        pair = context.args[0]
        outcome = context.args[1]

        message = f"""
📈 RESULT

{pair} → {"✅ WIN" if outcome.lower() == "win" else "❌ LOSS"}
"""
        await update.message.reply_text(message)

    except:
        await update.message.reply_text("❌ Use: /result EURUSD WIN")

# Start bot
app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("signal", signal))
app.add_handler(CommandHandler("result", result))

print("Bot is running...")

app.run_polling()

if __name__ == "__main__":
    application.run_polling(drop_pending_updates=True)

    import time

current_time = int(time.time())

# Store when signal created
signal_time = current_time

# Ignore if older than 60 sec
if int(time.time()) - signal_time > 60:

import os

if __name__ == "__main__":
    app.run_polling(drop_pending_updates=True)