from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from telegram.request import HTTPXRequest
import random
from datetime import datetime, timedelta

TOKEN = "8639623533:AAFypjCIe5q2WIsTGe7Ws-P2eDVz3tAh2xY"

# RESULT FUNCTION (OUTSIDE)
async def send_result(context):
    chat_id = context.job.chat_id

    result = random.choices(
        ["✅ WIN", "❌ LOSS"],
        weights=[80, 20]
    )[0]

    await context.bot.send_message(
        chat_id=chat_id,
        text=f"""
━━━━━━━━━━━━━━━
🔥 *Signal Result*

{result}
━━━━━━━━━━━━━━━
""",
        parse_mode="Markdown"
    )

    # 🔥 IF LOSS → SEND MARTINGALE
    if result == "❌ LOSS":
        context.job_queue.run_once(send_martingale, 5, chat_id=chat_id)

async def send_martingale(context):
    chat_id = context.job.chat_id

    await context.bot.send_message(
        chat_id=chat_id,
        text="""
⚠️ *MARTINGALE 1*

Retry the same signal immediately.
""",
        parse_mode="Markdown"
    )

# START COMMAND
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🔥 Bot started! Signals will be sent automatically.")

# SIGNAL FUNCTION (REUSABLE)
async def send_signal(context):
    chat_id = context.job.chat_id

    pair = random.choice(["EUR/USD", "GBP/USD", "USD/JPY", "AUD/USD"])
    timeframe = "1 Min"

    now = datetime.now()
    entry_time = (now + timedelta(minutes=1)).strftime("%H:%M")

    direction = random.choice(["🔼 CALL", "🔽 PUT"])

    message = f"""
📊 *Dhanjay AI*
━━━━━━━━━━━━━━━
💱 Pair: {pair} 

📈 Direction: {direction}

⏱ Expiry: {timeframe}  
━━━━━━━━━━━━━━━
⚡ Entry Time: {entry_time} 
🔥 Accuracy: 90%  
"""

    await context.bot.send_message(
        chat_id=chat_id,
        text=message,
        parse_mode="Markdown"
    )

    # ✅ schedule result AFTER signal
    context.job_queue.run_once(send_result, 60, chat_id=chat_id)

# STOP FUNCTION (FIXED)
async def stop_signals(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id

    jobs = context.job_queue.get_jobs_by_name(str(chat_id))
    for job in jobs:
        job.schedule_removal()

    await update.message.reply_text("🛑 Auto signals stopped!")

# AUTO SIGNAL FUNCTION
async def start_signals(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id

    # remove old jobs (important)
    jobs = context.job_queue.get_jobs_by_name(str(chat_id))
    for job in jobs:
        job.schedule_removal()

    # start new repeating job
    context.job_queue.run_repeating(
        send_signal,
        interval=60,
        first=0,
        chat_id=chat_id,
        name=str(chat_id)
    )

    await update.message.reply_text("🚀 Auto signals started!")

# ERROR HANDLER (MOVE BEFORE RUN)
async def error_handler(update, context):
    print(f"Error: {context.error}")

# REQUEST
request = HTTPXRequest(connect_timeout=30.0, read_timeout=30.0)

# APP
app = Application.builder().token("8639623533:AAFypjCIe5q2WIsTGe7Ws-P2eDVz3tAh2xY").request(request).build()

# HANDLERS
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("autosignal", start_signals))
app.add_handler(CommandHandler("stop", stop_signals))  # ✅ ADDED

app.add_error_handler(error_handler)

print("Bot running...")

import os
TOKEN = os.getenv("8639623533:AAFypjCIe5q2WIsTGe7Ws-P2eDVz3tAh2xY")# RUN
app.run_polling()
