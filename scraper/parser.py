import re
from datetime import datetime
from .models import Record

class Parser:
    def parse_wikipedia_page(self, page_data: dict) -> Record:
        page_id = str(page_data.get("pageid"))
        title = page_data.get("title", "")
        raw_text = page_data.get("extract", "")

        clean_text = self._clean_text(raw_text)

        cats = [c.get("title", "").replace("Категорија:", "") for c in page_data.get("categories", [])]

        return Record(
            id=page_id,
            title=title,
            site_url="https://mk.wikipedia.org", # Ова фалеше
            page_url=f"https://mk.wikipedia.org/wiki/{title.replace(' ', '_')}",
            content=clean_text,
            published_at=None,                   # Ова фалеше
            categories=cats,
            scraped_at=datetime.now().isoformat()
        )

    def _clean_text(self, text: str) -> str:
        if not text: return ""
        text = re.sub(r'\[\d+\]', '', text)
        text = re.sub(r'\[уреди.*?\]', '', text)
        text = re.sub(r'\n{3,}', '\n\n', text)
        return text.strip()