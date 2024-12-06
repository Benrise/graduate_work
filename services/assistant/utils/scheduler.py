from typing import Callable
import asyncio


async def scheduler(callback: Callable, interval_minutes: int = 30):
    while True:
        await callback()
        await asyncio.sleep(interval_minutes * 60)
