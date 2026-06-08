import os
import yt_dlp
from gtts import gTTS
from telegram.ext import ApplicationBuilder, MessageHandler, filters

def process_audio(url):
    ydl_opts = {'format': 'bestaudio', 'outtmpl': 'input.mp3', 'postprocessors': [{'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3'}]}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl: ydl.download([url])
    tts = gTTS("ဗီဒီယိုမှ အသံကို ပြောင်းလဲပြီးပါပြီ။", lang='my')
    tts.save("output.mp3")

async def handle_message(update, context):
    url = update.message.text
    if "youtube.com" in url or "youtu.be" in url:
        await update.message.reply_text("လုပ်ဆောင်နေပါပြီ...")
        process_audio(url)
        await update.message.reply_audio(audio=open("output.mp3", "rb"))

if __name__ == "__main__":
    app = ApplicationBuilder().token(os.environ["BOT_TOKEN"]).build()
    app.add_handler(MessageHandler(filters.TEXT, handle_message))
    app.run_polling()
