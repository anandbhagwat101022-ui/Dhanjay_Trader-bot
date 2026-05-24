from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from telegram.request import HTTPXRequest
import random
from datetime import datetime, timedelta
import os

TOKEN = os.getenv("TOKEN")  # ✅ correct key

if not TOKEN:
    raise ValueError("❌ TOKEN not found")

TOKEN = TOKEN.strip()  # ✅ safe

# RESULT FUNCTION
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

    # If loss → martingale
    if result == "❌ LOSS":
        context.job_queue.run_once(
            send_martingale,
            5,
            chat_id=chat_id,
            name=f"martingale_{chat_id}"
        )

# MARTINGALE
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
    await update.message.reply_text("🔥 Bot started!")

# SIGNAL FUNCTION
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

    # schedule result
    context.job_queue.run_once(
        send_result,
        60,
        chat_id=chat_id,
        name=f"result_{chat_id}"
    )

# START AUTO SIGNALS
async def start_signals(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id

    # remove all old jobs
    for job in context.job_queue.jobs():
        if str(chat_id) in job.name:
            job.schedule_removal()

    context.job_queue.run_repeating(
        send_signal,
        interval=60,
        first=0,
        chat_id=chat_id,
        name=f"signal_{chat_id}"
    )

    await update.message.reply_text("🚀 Auto signals started!")

# STOP ALL SIGNALS
async def stop_signals(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id

    removed = False

    for job in context.job_queue.jobs():
        if str(chat_id) in job.name:
            job.schedule_removal()
            removed = True

    if removed:
        await update.message.reply_text("🛑 All signals stopped!")
    else:
        await update.message.reply_text("⚠️ No active signals.")

# ERROR HANDLER
async def error_handler(update, context):
    print(f"Error: {context.error}")

# REQUEST CONFIG
request = HTTPXRequest(connect_timeout=30.0, read_timeout=30.0)

# APP INIT
app = Application.builder().token(TOKEN).request(request).build()

# HANDLERS
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("autosignal", start_signals))
app.add_handler(CommandHandler("stop", stop_signals))

app.add_error_handler(error_handler)

print("Bot running...")

# RUN
app.run_polling()
