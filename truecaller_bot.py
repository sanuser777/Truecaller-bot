import os
import logging
from telegram.ext import ApplicationBuilder, CommandHandler
from telegram import Update
from telegram.ext import ContextTypes
import requests

logging.basicConfig(level=logging.INFO)
TOKEN = os.environ.get("TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello! Use /whois <number> to search.")

async def whois(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Send number like /whois 9876543210")
        return

    number = context.args[0].replace("+", "").replace(" ", "")
    url = f"https://html.duckdns.org/tc.php?number=IN{number}"

    try:
        r = requests.get(url).json()
        name = r.get("name", "Not found")
        spam = r.get("spam", "N/A")
        city = r.get("city", "Unknown")
        await update.message.reply_text(f"📞 Name: {name}\n📍 City: {city}\n⚠️ Spam: {spam}%\n\n🔢 Number: {number}")
    except Exception:
        await update.message.reply_text("❌ Error fetching number info.")

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("whois", whois))
app.run_polling()
