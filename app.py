import os
import yt_dlp
import asyncio
from gtts import gTTS
from telegram.ext import ApplicationBuilder, MessageHandler, filters

# အသံဖိုင်ထုတ်လုပ်ခြင်း function
def process_audio(url):
    # ဗီဒီယို တစ်ခုလုံးမဆွဲဘဲ အသံ (bestaudio) ကိုသာ ဆွဲယူပါ
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3', 'preferredquality': '128'}],
        'outtmpl': 'input.mp3',
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    
    # ဤနေရာတွင် စာသားဘာသာပြန်ရန်အတွက် လိုအပ်လျှင် Googletrans ကို ဆက်ထည့်နိုင်ပါသည်
    # လောလောဆယ် စမ်းသပ်ရန်အတွက် အသံဖိုင်ကို အဆင်သင့်လုပ်ထားခြင်း
    tts = gTTS("ဗီဒီယိုမှ အသံကို အောင်မြင်စွာ ထုတ်ယူပြီးပါပြီ", lang='my')
    tts.save("output.mp3")

async def handle_message(update, context):
    url = update.message.text
    if "youtube.com" in url or "youtu.be" in url:
        await update.message.reply_text("ဗီဒီယိုကို လုပ်ဆောင်နေပါပြီ... ခဏစောင့်ပါ...")
        
        try:
            loop = asyncio.get_event_loop()
            await loop.run_in_executor(None, process_audio, url)
            
            if os.path.exists("output.mp3"):
                await update.message.reply_audio(audio=open("output.mp3", "rb"))
            else:
                await update.message.reply_text("အသံဖိုင် ထုတ်ယူရာတွင် အမှားအယွင်းရှိပါသည်။")
        except Exception as e:
            await update.message.reply_text(f"Error: {str(e)}")
    else:
        await update.message.reply_text("ကျေးဇူးပြု၍ YouTube link ကို ပို့ပေးပါ။")

# Flask နှင့် Telegram Bot ကို run သည့် အပိုင်းကို မူလအတိုင်း ထားပါ
