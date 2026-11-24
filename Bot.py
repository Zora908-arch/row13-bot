
import os
import telebot
from flask import Flask, request

TOKEN = os.environ.get("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)

app = Flask(__name__)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(
        message,
        "🎬 Welcome to Row 13!\n\n"
        "A cozy place for movie lovers.\n"
        "Let's talk movies! 🍿"
    )

@app.route('/')
def home():
    return "Row 13 Bot is running!"

@app.route('/' + TOKEN, methods=['POST'])
def webhook():
    json_data = request.get_json()
    update = telebot.types.Update.de_json(json_data)
    bot.process_new_updates([update])
    return "OK", 200

if __name__ == '__main__':
    url = os.environ.get("RENDER_EXTERNAL_URL")
    bot.remove_webhook()
    bot.set_webhook(url=url + '/' + TOKEN)
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 10000)))
