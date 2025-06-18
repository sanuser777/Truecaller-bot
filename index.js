require('dotenv').config();
const TelegramBot = require('node-telegram-bot-api');
const axios = require('axios');
const express = require('express');
const app = express();
const PORT = process.env.PORT || 3000;

// Telegram Bot
const bot = new TelegramBot(process.env.BOT_TOKEN, { polling: true });

bot.onText(/\/start/, (msg) => {
  bot.sendMessage(msg.chat.id, '📞 Send a phone number with country code.\nExample: +919876543210');
});

bot.on('message', async (msg) => {
  const chatId = msg.chat.id;
  const number = msg.text;

  if (!number.startsWith('+91')) return;

  try {
    const res = await axios.get(`https://raganork-api.onrender.com/true?number=${number}`);
    const data = res.data;

    if (!data || !data.name) return bot.sendMessage(chatId, '❌ No result found.');

    let reply = `👤 *Name:* ${data.name}\n`;
    if (data.email) reply += `📧 *Email:* ${data.email}\n`;
    if (data.carrier) reply += `📡 *Carrier:* ${data.carrier}\n`;
    if (data.timezone) reply += `🌐 *TimeZone:* ${data.timezone}\n`;
    if (data.city) reply += `🏙️ *City:* ${data.city}`;

    bot.sendMessage(chatId, reply, { parse_mode: 'Markdown' });

  } catch (e) {
    bot.sendMessage(chatId, '⚠️ Error fetching info.');
  }
});

// Express Ping Route
app.get('/', (req, res) => {
  res.send('✅ Telegram Truecaller Bot is alive!');
});

app.listen(PORT, () => {
  console.log(`🌐 Web server running on http://localhost:${PORT}`);
});
