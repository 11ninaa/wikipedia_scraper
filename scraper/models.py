from dataclasses import dataclass, field
from typing import Optional, List

@dataclass
class Record:
    id: str
    title: str
    site_url: str
    page_url: str
    content: Optional[str] = None
    published_at: Optional[str] = None
    categories: List[str] = field(default_factory=list)
    metadata: dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "title": self.title,
            "site_url": self.site_url,
            "page_url": self.page_url,
            "content": self.content,
            "published_at": self.published_at,
            "categories": self.categories,
            "metadata": self.metadata,
        }