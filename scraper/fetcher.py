from typing import Optional, List
from config import settings
from .http_client import HttpClient

class Fetcher:
    def __init__(self, http_client: HttpClient):
        self.http = http_client

    async def fetch_category_members(self, category_name: str) -> List[dict]:
        params = {
            "action": "query",
            "list": "categorymembers",
            "cmtitle": f"Категорија:{category_name}",
            "cmlimit": 50,
            "format": "json",
            "formatversion": 2
        }
        data = await self.http.fetch_json(settings.site_url, params=params)
        return data.get("query", {}).get("categorymembers", []) if data else []

    async def fetch_article_content(self, page_id: str) -> Optional[dict]:
        params = {
            "action": "query",
            "pageids": page_id,
            "prop": "extracts|categories",
            "explaintext": 1,
            "format": "json",
            "formatversion": 2
        }
        data = await self.http.fetch_json(settings.site_url, params=params)
        if data:
            pages = data.get("query", {}).get("pages", [])
            return pages[0] if pages else None
        return None