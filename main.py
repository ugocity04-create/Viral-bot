import os
import random
import asyncio
from datetime import datetime
from telegram import Bot
import edge_tts
from moviepy.editor import *
from PIL import Image

# 🔧 FIX ANTIALIAS ERROR
Image.ANTIALIAS = Image.Resampling.LANCZOS

BOT_TOKEN = "7744382374:AAFSXZBzimLxVww7q-uDhZVFVvN2tUX_yoU"
USER_ID = 7968704335

# ==============================
# CONTENT ENGINE
# ==============================
hooks = [
    "90% of traders lose because of this",
    "Stop trading until you understand this",
    "This mistake is destroying your account",
]

bodies = [
    "You are overtrading and forcing entries",
    "You risk too much per trade",
    "You trade without confirmation",
    "You let emotions control your decisions",
]

endings = [
    "Discipline is everything",
    "Patience makes profitable traders",
    "Control risk and you win",
    "Trade less, win more",
]

def generate_script():
    text = f"{random.choice(hooks)}. {random.choice(bodies)}. {random.choice(endings)}."
    text += " Follow for real trading discipline."
    return text

# ==============================
# VOICE
# ==============================
async def generate_voice(text):
    tts = edge_tts.Communicate(text, voice="en-US-AriaNeural")
    await tts.save("voice.mp3")

# ==============================
# VIDEO
# ==============================
def get_video(duration):
    clip = VideoFileClip("videos/bg1.mp4")

    if clip.duration < duration:
        clip = clip.loop(duration=duration)

    return clip.subclip(0, duration).resize((1080,1920))

def create_video(text):
    asyncio.run(generate_voice(text))

    audio = AudioFileClip("voice.mp3")
    duration = audio.duration

    bg = get_video(duration)

    txt = TextClip(
        text,
        fontsize=60,
        color='white',
        size=(900, None),
        method='caption'
    ).set_position(("center","center")).set_duration(duration)

    video = CompositeVideoClip([bg, txt])
    video = video.set_audio(audio)

    filename = f"video_{datetime.now().strftime('%H%M%S')}.mp4"
    video.write_videofile(filename, fps=24)

    return filename

# ==============================
# TELEGRAM
# ==============================
async def send_video(bot, path):
    with open(path, "rb") as vid:
        await bot.send_video(chat_id=USER_ID, video=vid)

# ==============================
# MAIN LOOP
# ==============================
async def main():
    bot = Bot(token=BOT_TOKEN)

    while True:
        try:
            print("🔥 Creating viral content...")

            text = generate_script()
            video_path = create_video(text)

            await send_video(bot, video_path)

            print("✅ Sent successfully!")

        except Exception as e:
            print(f"❌ Error: {e}")

        await asyncio.sleep(18000)  # 5 hours

if __name__ == "__main__":
    asyncio.run(main())



