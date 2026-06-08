import os
import tempfile
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from gtts import gTTS
import ffmpeg

# Logging ထည့်ထားခြင်းဖြင့် Error ဘယ်မှာတက်လဲ သိနိုင်မယ်
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

BOT_TOKEN = os.getenv("BOT_TOKEN")
PORT = int(os.environ.get("PORT", 8080))

async def handle_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📥 Processing your video...")

    video_path = tempfile.NamedTemporaryFile(suffix=".mp4", delete=False).name
    output_audio = tempfile.NamedTemporaryFile(suffix=".mp3", delete=False).name

    try:
        # Video ဖိုင်ကို ဒေါင်းလုပ်ဆွဲခြင်း
        file = await update.message.video.get_file()
        await file.download_to_drive(video_path)

        # ffmpeg ဖြင့် Audio ထုတ်ယူခြင်း (mp3 အဖြစ်)
        ffmpeg.input(video_path).output(output_audio, ac=1, ar="16000", vn=None).run(overwrite_output=True)

        # Voice message အဖြစ် ပြန်ပို့ခြင်း
        with open(output_audio, "rb") as f:
            await update.message.reply_voice(f)

    except Exception as e:
        logging.error(f"Error: {e}")
        await update.message.reply_text("Error ဖြစ်သွားပါပြီ၊ နောက်တစ်ခါ ထပ်စမ်းကြည့်ပါ။")

    finally:
        # အသုံးပြုပြီး ဖိုင်များကို ဖျက်ခြင်း
        for p in [video_path, output_audio]:
            if os.path.exists(p):
                os.remove(p)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🎬 Bot is alive and ready!")

def main():
    if not BOT_TOKEN:
        print("Error: BOT_TOKEN is missing!")
        return

    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.VIDEO, handle_video))

    print("Bot started...")
    # Render မှာ run ရင် polling_poll ကို သုံးပါတယ်
    app.run_polling()

if __name__ == "__main__":
    main()
