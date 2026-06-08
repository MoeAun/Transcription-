import os
import threading
from flask import Flask
from telegram.ext import ApplicationBuilder

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running!"

def run_flask():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

def run_bot():
    token = os.environ.get("BOT_TOKEN")
    if not token:
        print("CRITICAL ERROR: BOT_TOKEN is missing!")
        return
    
    # Bot ကို အသစ်ဆောက်ပါ
    app_bot = ApplicationBuilder().token(token).build()
    
    # ဤနေရာတွင် မည်သည့် Handler မှ မထည့်ရသေးပါက Bot က စာမပြန်ပါ
    # စမ်းသပ်ရန်အတွက် အောက်ပါ handler လေးထည့်ပါ
    from telegram.ext import CommandHandler
    async def start(update, context):
        await update.message.reply_text("Bot အလုပ်လုပ်နေပါပြီ!")
    
    app_bot.add_handler(CommandHandler("start", start))
    
    print("Bot is polling...") # ဒီစာသား Log မှာ ပေါ်မှ Bot အလုပ်လုပ်မှာ
    app_bot.run_polling()

if __name__ == "__main__":
    # Flask ကို Background မှာ run
    threading.Thread(target=run_flask).start()
    # Bot ကို main thread မှာ run
    run_bot()
