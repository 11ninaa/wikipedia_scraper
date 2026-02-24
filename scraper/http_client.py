import aiohttp
import asyncio
from typing import Any, Optional, Dict
from utils import RateLimiter, retry_on_exception
from config import settings

class HttpClient:
    def __init__(self, session: aiohttp.ClientSession):
        self.session = session
        self.rate_limiter = RateLimiter(settings.requests_per_second)

    @retry_on_exception(
        max_retries=settings.max_retries,
        delay=settings.retry_delay,
        backoff=settings.retry_backoff,
        exceptions=(aiohttp.ClientError, asyncio.TimeoutError),
    )
    async def fetch_json(self, url: str, params: Optional[Dict] = None) -> Optional[Any]:
        await self.rate_limiter.wait()
        async with self.session.get(url, params=params, headers=settings.headers) as response:
            response.raise_for_status()
            return await response.json()