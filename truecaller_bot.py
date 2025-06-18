import os
import logging
from telegram.ext import ApplicationBuilder, CommandHandler
from telegram import Update
from telegram.ext import ContextTypes
import requests
from bs4 import BeautifulSoup

logging.basicConfig(level=logging.INFO)
TOKEN = os.environ.get("TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello! Use /whois <number> to search.")

async def whois(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Send number like /whois 9876543210")
        return

    number = context.args[0]
    url = f"https://www.truecaller.com/in/{number}"
    headers = {'User-Agent': 'Mozilla/5.0'}

    try:
        r = requests.get(url, headers=headers)
        soup = BeautifulSoup(r.text, "html.parser")
        name = soup.find("h1").text.strip() if soup.find("h1") else "Not Found"
        await update.message.reply_text(f"Name: {name}\nNumber: {number}")
    except Exception:
        await update.message.reply_text("Failed to fetch data.")

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("whois", whois))
app.run_polling()
