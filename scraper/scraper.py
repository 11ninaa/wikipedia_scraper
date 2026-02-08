import asyncio
import logging
import os
import aiohttp
from datetime import datetime
from config import settings
from scraper.fetcher import Fetcher
from scraper.parser import Parser
from store import JSONFileStore
from scraper.models import Record

logger = logging.getLogger(__name__)


class Scraper:
    def __init__(self, site_url: str, site_name: str):
        self._site_url = site_url
        self.main_file = os.path.abspath("results.json")
        self.seen_file = os.path.abspath("seen-ids.json")

        print(f"\n--- Start ---")
        print(f"File: {self.main_file}")

        self._store = JSONFileStore(self.main_file, self.seen_file)
        self._parser = Parser()

    async def run(self):
        async with aiohttp.ClientSession() as session:
            print("Testing...")
            test_record = Record(
                id="test",
                title="Test",
                site_url="https://mk.wikipedia.org",
                page_url="https://mk.wikipedia.org/test",
                content=" ",
                scraped_at=datetime.now().isoformat()
            )

            self._store.save_records([test_record])
            print("Testing complete.")

            cat = settings.root_category if hasattr(settings, 'root_category') else "Македонија"
            await self._scrape_category(cat, depth=0, session=session)

    async def _scrape_category(self, category_name: str, depth: int, session: aiohttp.ClientSession):
        max_d = settings.max_depth if hasattr(settings, 'max_depth') else 2
        if depth > max_d:
            return

        fetcher = Fetcher(session)
        print(f"Category: {category_name} (Level {depth})")

        try:
            members = await fetcher.fetch_category_members(category_name)

            for member in members:
                page_id = str(member.get("pageid"))
                if member.get("ns") == 0:
                    is_seen = False
                    try:
                        if hasattr(self._store, 'seen_ids'):
                            is_seen = page_id in self._store.seen_ids
                    except:
                        pass

                    if not is_seen:
                        raw_data = await fetcher.fetch_article_content(page_id)
                        if raw_data:
                            record = self._parser.parse_wikipedia_page(raw_data)
                            self._store.save_records([record])
                            print(f"Successfully saved: {member.get('title')}")
                        await asyncio.sleep(0.5)

                elif member.get("ns") == 14:
                    raw_title = member.get("title", "")
                    sub_cat = raw_title.replace("Категорија:", "").replace("Category:", "").strip()
                    await self._scrape_category(sub_cat, depth + 1, session)

        except Exception as e:
            print(f"Error: {e}")