import os
import tempfile
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from gtts import gTTS
import ffmpeg

BOT_TOKEN = "8901325853:AAGitB0XPJf5SFS17NHj80d3g9cFSSBGP9Q"

async def handle_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Processing your video...")
    
    video_path = tempfile.NamedTemporaryFile(suffix=".mp4", delete=False).name
    audio_path = tempfile.NamedTemporaryFile(suffix=".wav", delete=False).name
    output_audio = tempfile.NamedTemporaryFile(suffix=".mp3", delete=False).name
    
    try:
        # Download video
        file = await update.message.video.get_file()
        await file.download_to_drive(video_path)
        
        # Extract audio
        ffmpeg.input(video_path).output(audio_path, ac=1, ar="16000").run(quiet=True, overwrite_output=True)
        
        # Generate test voice
        tts = gTTS(text="Hello, your bot is working on Render", lang="en", slow=False)
        tts.save(output_audio)
        
        # Send response
        await update.message.reply_text("✅ Done! Here is your audio.")
        with open(output_audio, "rb") as f:
            await update.message.reply_voice(voice=f)
            
    except Exception as e:
        await update.message.reply_text(f"Error: {str(e)[:200]}")
    finally:
        for path in [video_path, audio_path, output_audio]:
            if os.path.exists(path):
                os.unlink(path)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🎬 Bot is alive! Send me a video.")

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.VIDEO, handle_video))
    print("🤖 Bot is running on Render.com...")
    app.run_polling()

if __name__ == "__main__":
    main()
