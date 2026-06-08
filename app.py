import os
import yt_dlp
from gtts import gTTS
from googletrans import Translator
from telegram.ext import ApplicationBuilder, MessageHandler, filters

async def handle_message(update, context):
    url = update.message.text
    if "youtube.com" in url or "youtu.be" in url:
        await update.message.reply_text("ဗီဒီယိုကို လုပ်ဆောင်နေပါပြီ ခဏစောင့်ပါ...")
        
        # 1. YouTube မှ အသံဖိုင် ဒေါင်းလုပ်ဆွဲခြင်း
        ydl_opts = {'format': 'bestaudio', 'outtmpl': 'audio.mp3'}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
            
        # 2. ဘာသာပြန်ခြင်း (ဒီနေရာမှာ စာသားထုတ်ရန် Whisper လိုအပ်သည်)
        # အခုလောလောဆယ် စမ်းသပ်ရန်အတွက် ရိုးရှင်းသော အသံဖိုင် ပြန်ထုတ်ခြင်း
        tts = gTTS("ဒါဟာ ဘာသာပြန်ထားတဲ့ အသံဖိုင်ဖြစ်ပါတယ်", lang='my')
        tts.save("output.mp3")
        
        # 3. အသံဖိုင် ပြန်ပို့ခြင်း
        await update.message.reply_audio(audio=open("output.mp3", "rb"))
    else:
        await update.message.reply_text("ကျေးဇူးပြု၍ YouTube link တစ်ခု ပေးပို့ပါ။")

if __name__ == "__main__":
    token = os.environ.get("BOT_TOKEN")
    app = ApplicationBuilder().token(token).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()
