import asyncio
import logging
import sys
from config import settings
from scraper.scraper import Scraper

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=sys.stdout
)
logger = logging.getLogger(__name__)


async def main():
    print("\n" + "=" * 40)
    print("Starting the scraper...")
    print("=" * 40 + "\n")

    try:
        scraper = Scraper(site_url=settings.site_url, site_name=settings.site_name)

        await scraper.run()

    except Exception as e:
        logger.error(f"Error: {e}", exc_info=True)

    print("\n" + "=" * 40)
    print("Scraping has ended")
    print("=" * 40)


if __name__ == "__main__":
    asyncio.run(main())