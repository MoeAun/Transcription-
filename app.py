import os
import yt_dlp
import asyncio
from gtts import gTTS
from telegram.ext import ApplicationBuilder, MessageHandler, filters

# အသံဖိုင်ထုတ်လုပ်ခြင်း function
def process_audio(url):
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3', 'preferredquality': '192'}],
        'outtmpl': 'input.mp3',
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    
    tts = gTTS("ဗီဒီယိုမှ အသံကို အောင်မြင်စွာ ပြောင်းလဲပြီးပါပြီ။", lang='my')
    tts.save("output.mp3")

async def handle_message(update, context):
    url = update.message.text
    await update.message.reply_text("လုပ်ဆောင်နေပါပြီ... ခဏစောင့်ပါ...")
    
    try:
        # loop.run_in_executor ကိုသုံးခြင်းက thread ထက် ပိုပြီး telegram bot နဲ့ အဆင်ပြေပါတယ်
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, process_audio, url)
        
        # ဖိုင်ထုတ်ပြီးမှ ပြန်ပို့ခြင်း
        if os.path.exists("output.mp3"):
            await update.message.reply_audio(audio=open("output.mp3", "rb"))
        else:
            await update.message.reply_text("ဖိုင်ထုတ်ယူရာတွင် အမှားအယွင်းရှိနေပါသည်။")
            
    except Exception as e:
        await update.message.reply_text(f"Error တက်သွားပါသည်: {str(e)}")

# (Flask run_flask code ကို အောက်တွင် ပုံမှန်အတိုင်း ထားပါ)
