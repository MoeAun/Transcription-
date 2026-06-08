import os
import logging
import threading
import yt_dlp
import whisper
from googletrans import Translator
from gtts import gTTS
from flask import Flask
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Setup
logging.basicConfig(level=logging.INFO)
PORT = int(os.environ.get("PORT", 8080))
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Flask Health Check
server = Flask(__name__)
@server.route('/')
def home(): return "Bot is running", 200

# Bot Logic
async def process_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text
    await update.message.reply_text("⏳ Processing... ကျေးဇူးပြု၍ ခဏစောင့်ပေးပါ။")

    try:
        # 1. Download Audio
        ydl_opts = {'format': 'bestaudio/best', 'outtmpl': 'audio.mp3'}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl: ydl.download([url])

        # 2. Transcribe (Whisper tiny)
        model = whisper.load_model("tiny")
        result = model.transcribe("audio.mp3")
        eng_text = result["text"]

        # 3. Translate to Burmese
        translator = Translator()
        mm_text = translator.translate(eng_text, dest='my').text

        # 4. Text-to-Speech
        tts = gTTS(text=mm_text, lang='my')
        tts.save("output.mp3")

        # 5. Send Audio
        with open("output.mp3", "rb") as f:
            await update.message.reply_voice(voice=f, caption="✅ ဘာသာပြန်ပြီးပါပြီ။")

    except Exception as e:
        await update.message.reply_text(f"Error: {str(e)}")
    finally:
        for f in ["audio.mp3", "output.mp3"]:
            if os.path.exists(f): os.remove(f)

def run_bot():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", lambda u, c: u.message.reply_text("YouTube Link ပို့ပေးပါ")))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, process_video))
    app.run_polling()

if __name__ == "__main__":
    threading.Thread(target=lambda: server.run(host='0.0.0.0', port=PORT)).start()
    run_bot()
