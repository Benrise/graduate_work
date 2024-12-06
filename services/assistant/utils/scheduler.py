import asyncio
from typing import Callable


async def scheduler(callback: Callable, interval_minutes: int = 30):
    while True:
        await callback()
        await asyncio.sleep(interval_minutes * 60)
