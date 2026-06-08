import os
import yt_dlp
from flask import Flask
from threading import Thread
from telegram.ext import Application, MessageHandler, filters

# Server အသက်ဝင်ဖို့ (Render က Ping ဖို့)
app_flask = Flask(__name__)
@app_flask.route('/')
def home(): return "Bot is running!"

def run_flask(): 
    app_flask.run(host='0.0.0.0', port=int(os.environ.get("PORT", 8080)))

# Bot Logic
async def handle_msg(update, context):
    await update.message.reply_text("စမ်းသပ်နေပါတယ်... အဆင်ပြေပါတယ်ခင်ဗျာ။")

if __name__ == "__main__":
    # Flask Server ကို background မှာ run
    Thread(target=run_flask).start()
    
    # Bot ကို run
    token = os.getenv("BOT_TOKEN")
    app = Application.builder().token(token).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_msg))
    app.run_polling()
