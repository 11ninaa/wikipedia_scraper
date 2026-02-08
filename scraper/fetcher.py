import aiohttp
import logging
from typing import Any, Optional, List
from config import settings

logger = logging.getLogger(__name__)


class Fetcher:
    def __init__(self, session: aiohttp.ClientSession):
        self.session = session

    async def fetch_category_members(self, category_name: str) -> List[dict]:
        params = {
            "action": "query",
            "list": "categorymembers",
            "cmtitle": f"Категорија:{category_name}",
            "cmlimit": 50,
            "format": "json",
            "formatversion": 2
        }

        async with self.session.get(settings.site_url, params=params, headers=settings.headers) as resp:
            if resp.status == 403:
                logger.error("Error")
                return []

            if resp.status != 200:
                logger.error(f"Error: {resp.status}")
                return []

            data = await resp.json()
            return data.get("query", {}).get("categorymembers", [])

    async def fetch_article_content(self, page_id: str) -> Optional[dict]:
        params = {
            "action": "query",
            "pageids": page_id,
            "prop": "extracts|categories",
            "explaintext": 1,
            "format": "json",
            "formatversion": 2
        }
        async with self.session.get(settings.site_url, params=params, headers=settings.headers) as resp:
            if resp.status != 200:
                return None
            data = await resp.json()
            pages = data.get("query", {}).get("pages", [])
            return pages[0] if pages else None