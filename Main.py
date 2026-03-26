import os
import random
import asyncio
import time
from datetime import datetime

import imageio_ffmpeg
from moviepy.editor import *
import edge_tts

# Force ffmpeg (Railway supports this perfectly)
os.environ["IMAGEIO_FFMPEG_EXE"] = imageio_ffmpeg.get_ffmpeg_exe()

# ==============================
# CONTENT
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
    text += " Follow for real trading discipline. DM me START to learn."
    return text

async def generate_voice(text):
    tts = edge_tts.Communicate(text, voice="en-US-AriaNeural")
    await tts.save("voice.mp3")

def get_random_background(duration):
    folder = "videos"

    if not os.path.exists(folder):
        os.makedirs(folder)

    files = [f for f in os.listdir(folder) if f.endswith(".mp4")]

    if not files:
        raise Exception("Upload videos into /videos folder")

    clip = VideoFileClip(os.path.join(folder, random.choice(files)))

    if clip.duration < duration:
        clip = clip.loop(duration=duration)

    return clip.subclip(0, duration).resize((1080, 1920))

def create_video():
    text = generate_script()
    filename = f"viral_{datetime.now().strftime('%H%M%S')}.mp4"

    asyncio.run(generate_voice(text))
    audio = AudioFileClip("voice.mp3")

    bg = get_random_background(audio.duration)

    video = bg.set_audio(audio)
    video.write_videofile(filename, fps=24)

    print("✅ Created", filename)

# ==============================
# LOOP (RUN EVERY 10 MINUTES)
# ==============================
print("🚀 BOT RUNNING...")

while True:
    try:
        create_video()
        time.sleep(600)  # 10 minutes
    except Exception as e:
        print("Error:", e)
        time.sleep(60)
