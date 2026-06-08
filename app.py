import os
import tempfile
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from gtts import gTTS
import ffmpeg

BOT_TOKEN = os.getenv("BOT_TOKEN")

async def handle_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Processing your video...")

    video_path = tempfile.NamedTemporaryFile(suffix=".mp4", delete=False).name
    audio_path = tempfile.NamedTemporaryFile(suffix=".wav", delete=False).name
    output_audio = tempfile.NamedTemporaryFile(suffix=".mp3", delete=False).name

    try:
        file = await update.message.video.get_file()
        await file.download_to_drive(video_path)

        ffmpeg.input(video_path).output(
            audio_path,
            ac=1,
            ar="16000"
        ).run(overwrite_output=True)

        tts = gTTS("Hello, your bot is working on Render", lang="en")
        tts.save(output_audio)

        with open(output_audio, "rb") as f:
            await update.message.reply_voice(f)

    except Exception as e:
        await update.message.reply_text(str(e))

    finally:
        for p in [video_path, audio_path, output_audio]:
            if os.path.exists(p):
                os.remove(p)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🎬 Bot is alive!")

def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.VIDEO, handle_video))

    print("Bot started...")
    app.run_polling()

if __name__ == "__main__":
    main()
