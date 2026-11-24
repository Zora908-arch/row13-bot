
import os
import time
import threading
import telebot
from flask import Flask, request

TOKEN = os.environ.get("BOT_TOKEN")
URL = os.environ.get("RENDER_EXTERNAL_URL")

if not TOKEN or not URL:
    raise RuntimeError("Missing BOT_TOKEN or RENDER_EXTERNAL_URL")

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

@app.route("/")
def home():
    return "Row 13 Bot is running!"

@app.route("/" + TOKEN, methods=["POST"])
def webhook():
    data = request.get_json()
    update = telebot.types.Update.de_json(data)
    bot.process_new_updates([update])
    return "OK", 200

@bot.message_handler(commands=["start"])
def start(message):
    bot.reply_to(
        message,
        "🎬 Welcome to Row 13!\n\n"
        "A cozy place for movie lovers.\n"
        "Let's talk movies! 🍿"
    )

def setup_webhook():
    target = URL + "/" + TOKEN

    while True:
        try:
            info = bot.get_webhook_info()

            if info.url != target:
                bot.set_webhook(url=target)

            print("Webhook connected successfully!")
            break

        except Exception as e:
            print("Webhook error:", e)
            time.sleep(30)

if __name__ == "__main__":
    threading.Thread(
        target=setup_webhook,
        daemon=True
    ).start()

    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 10000))
    )
