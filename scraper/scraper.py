import logging
import aiohttp
from config import settings
from store import StoreFactory
from .fetcher import Fetcher
from .parser import Parser
from .http_client import HttpClient

logger = logging.getLogger(__name__)


class Scraper:
    def __init__(self, site_url: str, site_name: str):
        self.site_url = site_url
        self.site_name = site_name
        self._store = StoreFactory.create(site_name)
        self._parser = Parser()

    async def run(self):
        async with aiohttp.ClientSession() as session:
            http_client = HttpClient(session)
            fetcher = Fetcher(http_client)

            root_cat = settings.root_category
            await self._scrape_category(root_cat, 0, fetcher)

    async def _scrape_category(self, category_name: str, depth: int, fetcher: Fetcher):
        if depth > settings.max_depth:
            return

        try:
            members = await fetcher.fetch_category_members(category_name)

            for member in members:
                page_id = str(member.get("pageid"))

                full_id = f"wiki_{page_id}"

                if full_id in self._store.seen_ids:
                    continue

                if member.get("ns") == 0:
                    raw_data = await fetcher.fetch_article_content(page_id)
                    if raw_data:
                        record = self._parser.parse_wikipedia_page(raw_data)
                        self._store.save_records([record])
                        logger.info(f"Saved: {record.title}")

                elif member.get("ns") == 14:
                    sub_cat = member.get("title", "").replace("Категорија:", "").strip()
                    await self._scrape_category(sub_cat, depth + 1, fetcher)

        except Exception as e:
            logger.error(f"Error in category {category_name}: {e}")