import os
import asyncio
from telegram import Bot

BOT_TOKEN = os.getenv("BOT_TOKEN")
USER_ID = os.getenv("USER_ID")

VIDEO_PATH = "videos/bg1.mp4"

async def send_video():
    bot = Bot(token=BOT_TOKEN)

    if not os.path.exists(VIDEO_PATH):
        print("❌ Error: Upload videos into /videos folder")
        return

    print("🚀 BOT RUNNING...")

    while True:
        try:
            with open(VIDEO_PATH, "rb") as video:
                await bot.send_video(chat_id=USER_ID, video=video)
                print("✅ Video sent!")

        except Exception as e:
            print(f"❌ Error: {e}")

        await asyncio.sleep(18000)  # 5 hours


if __name__ == "__main__":
    asyncio.run(send_video())

