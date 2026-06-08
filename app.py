import os
import threading
from flask import Flask
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters

# Railway Flask Server
app = Flask(__name__)
@app.route('/')
def home():
    return "Bot is running!"

def run_flask():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

# Bot Logic
async def start(update, context):
    await update.message.reply_text("Bot အဆင်သင့်ဖြစ်ပါပြီ!")

async def handle_message(update, context):
    await update.message.reply_text("လက်ခံရရှိပါပြီ။")

def run_bot():
    token = os.environ.get("BOT_TOKEN")
    if not token:
        print("Error: BOT_TOKEN မတွေ့ပါ")
        return
    
    bot_app = ApplicationBuilder().token(token).build()
    bot_app.add_handler(CommandHandler("start", start))
    bot_app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    print("Bot is polling...")
    bot_app.run_polling()

if __name__ == "__main__":
    threading.Thread(target=run_flask).start()
    run_bot()
