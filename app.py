import os
import yt_dlp
from flask import Flask
from threading import Thread
from telegram.ext import Application, MessageHandler, filters

# Server အသက်ဝင်ဖို့အတွက်
app_flask = Flask(__name__)
@app_flask.route('/')
def home(): return "Bot is running!"

def run_flask(): app_flask.run(host='0.0.0.0', port=int(os.environ.get("PORT", 8080)))

# Bot အလုပ်လုပ်ဖို့
async def handle_msg(update, context):
    await update.message.reply_text("စမ်းသပ်နေပါတယ်...")

if __name__ == "__main__":
    Thread(target=run_flask).start()
    app = Application.builder().token(os.getenv("BOT_TOKEN")).build()
    app.add_handler(MessageHandler(filters.TEXT, handle_msg))
    app.run_polling()
