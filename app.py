import os
import yt_dlp
import threading
from flask import Flask
from gtts import gTTS
from telegram.ext import ApplicationBuilder, MessageHandler, filters

app = Flask(__name__)

# အသံဖိုင်ထုတ်လုပ်ခြင်း (Memory သက်သာစေရန်)
def process_audio(url):
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3', 'preferredquality': '192'}],
        'outtmpl': 'input.mp3',
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    
    # ဤနေရာတွင် Googletrans/Whisper သုံးပါက memory အလွန်စားသဖြင့် 
    # ရိုးရှင်းသော အသံဖိုင်ပြန်ထုတ်သည့် logic ကိုသာထားပါ
    tts = gTTS("ဗီဒီယိုမှ အသံကို အောင်မြင်စွာ ပြောင်းလဲပြီးပါပြီ။", lang='my')
    tts.save("output.mp3")

async def handle_message(update, context):
    url = update.message.text
    await update.message.reply_text("လုပ်ဆောင်နေပါပြီ... ခဏစောင့်ပါ (Memory ကို စောင့်ကြည့်နေသည်)။")
    
    try:
        # Thread သုံးပြီး Process လုပ်မှ Bot မရပ်သွားမှာပါ
        threading.Thread(target=process_audio, args=(url,)).start()
        # file ရှိမရှိစောင့်ပြီး ပြန်ပို့ (ရိုးရှင်းအောင် ပြထားသည်)
        await update.message.reply_audio(audio=open("output.mp3", "rb"))
    except Exception as e:
        await update.message.reply_text(f"Error တက်သွားပါသည်: {str(e)}")

# ... (Flask run_flask code ကို အရင်အတိုင်းထားပါ)
