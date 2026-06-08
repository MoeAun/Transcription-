import os
import tempfile
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from gtts import gTTS
import ffmpeg

# ========== TOKEN ကို တိုက်ရိုက်ထည့်ပါ ==========
BOT_TOKEN = "8901325853:AAGitB0XPJf5SFS17NHj80d3g9cFSSBGP9Q"
# =============================================

async def handle_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🎬 Video လက်ခံရရှိပါပြီ။ စတင် processing လုပ်နေပါပြီ... (၂-၃ မိနစ်ခန့် ကြာနိုင်ပါတယ်)")
    
    video_path = tempfile.NamedTemporaryFile(suffix=".mp4", delete=False).name
    audio_path = tempfile.NamedTemporaryFile(suffix=".wav", delete=False).name
    output_audio = tempfile.NamedTemporaryFile(suffix=".mp3", delete=False).name
    
    try:
        # Step 1: Download video
        await update.message.reply_text("📥 Video download လုပ်နေပါပြီ...")
        file = await update.message.video.get_file()
        await file.download_to_drive(video_path)
        
        # Step 2: Extract audio
        await update.message.reply_text("🎧 Audio ထုတ်ယူနေပါပြီ...")
        ffmpeg.input(video_path).output(audio_path, ac=1, ar="16000").run(quiet=True, overwrite_output=True)
        
        # Step 3: Transcription (Placeholder for now)
        await update.message.reply_text("📝 စာသားပြောင်းနေပါပြီ...")
        transcribed_text = "ဒါက စမ်းသပ်မှု စာသားဖြစ်ပါတယ်။ Video ထဲက စကားပြောကို တကယ်ဖတ်ဖို့ Whisper model ထည့်သွင်းပေးဖို့ လိုပါသေးတယ်။"
        
        # Step 4: Translate
        await update.message.reply_text("🔄 ဘာသာပြန်နေပါပြီ...")
        translated_text = "This is a test translation. For actual video transcription, Whisper model needs to be properly installed."
        
        # Step 5: Text to Speech
        await update.message.reply_text("🔊 အသံဖိုင် ထုတ်ယူနေပါပြီ...")
        tts = gTTS(text=translated_text[:300], lang="en", slow=False)
        tts.save(output_audio)
        
        # Step 6: Send results
        await update.message.reply_text(
            f"**Original (မြန်မာ):**\n{transcribed_text[:400]}\n\n"
            f"**Translated (English):**\n{translated_text[:400]}",
            parse_mode="Markdown"
        )
        
        with open(output_audio, "rb") as f:
            await update.message.reply_voice(voice=f, caption="✅ ဘာသာပြန်ပြီးသော အသံဖိုင်")
            
    except Exception as e:
        await update.message.reply_text(f"⚠️ Error: {str(e)[:200]}")
    finally:
        for path in [video_path, audio_path, output_audio]:
            if os.path.exists(path):
                os.unlink(path)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🎬 **Video Translator Bot**\n\n"
        "Video တစ်ခု ပို့ပေးလိုက်ပါ။\n"
        "ကျွန်တော် ဘာသာပြန်ပေးပါမယ်။\n\n"
        "✅ Bot is running 24/7 on Render.com",
        parse_mode="Markdown"
    )

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.VIDEO, handle_video))
    print("🤖 Bot is running on Render.com...")
    app.run_polling()

if __name__ == "__main__":
    main()