import os
from aiogram import Dispatcher, Bot
from aiogram.filters import Command
from aiogram.types import Message
import asyncio
from prayer_uzbek_name import uzbek_names
from prayer_time import get_prayer_times
import pytz
from datetime import datetime

TOKEN = os.getenv("TOKEN")

bot = Bot(TOKEN)
dp = Dispatcher()

default_chat_id = None
sent_today = set()

@dp.message(Command("start"))
async def start_handler(message: Message):
    global default_chat_id
    default_chat_id = message.chat.id
    await message.answer("Assalomu alaykum. Men Kitob tumani namoz vaqtlarini eslatib turaman!")

async def eslatish():
    old_date = None
    timings = None

    while True:
        if default_chat_id:
            now_time = datetime.now(pytz.timezone("Asia/Tashkent"))
            today_str = now_time.strftime("%d-%m-%Y")
            now_hm = now_time.strftime("%H:%M")

            if old_date != today_str:
                timings = await get_prayer_times()
                sent_today.clear()
                old_date = today_str

            for name, time in timings.items():
                if now_hm == time[:5] and name not in sent_today:
                    text = f"⏰ {uzbek_names.get(name, name)} namozi vaqti bo‘ldi: {time}"
                    await bot.send_message(default_chat_id, text)
                    sent_today.add(name)

        await asyncio.sleep(60)

async def main():
    asyncio.create_task(eslatish())
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
