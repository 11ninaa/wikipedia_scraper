import re
from datetime import datetime
from vezilka_schemas import Record, RecordMeta, RecordType


class Parser:
    def parse_wikipedia_page(self, page_data: dict) -> Record:
        title = page_data.get("title", "")
        page_id = str(page_data.get("pageid"))
        extract = page_data.get("extract", "")

        tags = [c.get("title", "").replace("Категорија:", "").strip()
                for c in page_data.get("categories", [])]

        meta = RecordMeta(
            source="mk.wikipedia.org",
            url=f"https://mk.wikipedia.org/wiki/{title.replace(' ', '_')}",
            tags=tags,
            labels=[],
            scraped_at=datetime.now()
        )

        return Record(
            id=f"wiki_{page_id}",
            text=extract,
            type=RecordType.NARRATIVE,
            last_modified_at=datetime.now(),
            meta=meta
        )

    def _clean_text(self, text: str) -> str:
        if not text: return ""
        text = re.sub(r'\[\d+\]', '', text)
        text = re.sub(r'\[(уреди|edit).*?\]', '', text)
        return " ".join(text.split())