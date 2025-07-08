import aiohttp
from datetime import datetime

async def get_prayer_times(city="Kitob", country="Uzbekistan"):
    date_str = datetime.now().strftime("%d-%m-%Y")
    url = f"https://api.aladhan.com/v1/timingsByCity/{date_str}?city={city}&country={country}&method=2"

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            data = await resp.json()
            timings = data['data']['timings']
            return timings
