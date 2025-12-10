import asyncio
from aiogram import Bot, Dispatcher
from config import BOT_TOKEN
from database.models import create_tables
from handlers import start, video, admin

async def main():
    create_tables()
    bot = Bot(BOT_TOKEN)
    dp = Dispatcher()

    dp.include_router(admin.router)
    dp.include_router(start.router)
    dp.include_router(video.router)

    print("🤖 Bot is running...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
