import os
import random
import asyncio
from datetime import datetime
from telegram import Bot
import edge_tts
from moviepy.editor import *
from PIL import Image

# ✅ Fix Pillow issue
Image.ANTIALIAS = Image.Resampling.LANCZOS

# ✅ Use Railway variables
BOT_TOKEN = "7744382374:AAGdviU1Dge3EPTDrq20BJkaAXBxUyMASqw"
USER_ID = "7968704335"

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
# VOICE GENERATION
# ==============================
async def generate_voice(text):
    tts = edge_tts.Communicate(text, voice="en-US-AriaNeural")
    await tts.save("voice.mp3")

# ==============================
# VIDEO CREATION
# ==============================
from moviepy.editor import *
from PIL import Image, ImageDraw, ImageFont

def create_text_image(text, width=900, height=1600):
    img = Image.new("RGB", (width, height), color=(0, 0, 0))
    draw = ImageDraw.Draw(img)

    try:
        font = ImageFont.truetype("arial.ttf", 50)
    except:
        font = ImageFont.load_default()

    draw.multiline_text((50, 200), text, fill=(255, 255, 255), font=font, align="center")

    img.save("text.png")
    return "text.png"


def create_video(text):
    audio = AudioFileClip("voice.mp3")
    duration = audio.duration

    bg = VideoFileClip("videos/bg1.mp4")

    if bg.duration < duration:
        bg = bg.loop(duration=duration)

    bg = bg.subclip(0, duration).resize((1080, 1920))

    text_img = create_text_image(text)

    txt_clip = ImageClip(text_img).set_duration(duration).set_position("center")

    video = CompositeVideoClip([bg, txt_clip])
    video = video.set_audio(audio)

    filename = "final_video.mp4"
    video.write_videofile(filename, fps=24)

    return filename


# ==============================
# TELEGRAM SEND
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

            # ✅ FIXED (no asyncio.run)
            await generate_voice(text)

            video_path = create_video(text)

            await send_video(bot, video_path)

            print("✅ Sent successfully!")

        except Exception as e:
            print(f"❌ Error: {e}")

        await asyncio.sleep(18000)  # 5 hours


if __name__ == "__main__":
    asyncio.run(main())




