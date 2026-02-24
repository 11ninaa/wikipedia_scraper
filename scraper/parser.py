import re
from datetime import datetime
from .models import Record


class Parser:
    def parse_wikipedia_page(self, page_data: dict) -> Record:
        title = page_data.get("title", "")
        raw_text = page_data.get("extract", "")
        clean_text = self._clean_text(raw_text)
        page_id = str(page_data.get("pageid"))

        tags = [c.get("title", "").replace("Категорија:", "").strip()
                for c in page_data.get("categories", [])]

        return Record(
            id=f"wiki_{page_id}",
            title=title,
            site_url="https://mk.wikipedia.org",
            page_url=f"https://mk.wikipedia.org/wiki/{title.replace(' ', '_')}",
            content=clean_text,
            published_at=None,
            categories=tags,
            metadata={
                "source": "mk.wikipedia.org",
                "url": f"https://mk.wikipedia.org/wiki/{title.replace(' ', '_')}",
                "tags": tags,
                "labels": [],
                "scraped_at": datetime.now().isoformat(),
                "type": "NARRATIVE",  # Од сликата: RecordType.NARRATIVE
                "last_modified_at": datetime.now().isoformat()
            }
        )

    def _clean_text(self, text: str) -> str:
        if not text: return ""
        text = re.sub(r'\[\d+\]', '', text)
        text = re.sub(r'\[уреди.*?\]', '', text)
        text = re.sub(r'\n{3,}', '\n\n', text)
        return text.strip()