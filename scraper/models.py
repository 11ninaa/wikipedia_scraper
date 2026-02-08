from dataclasses import dataclass, asdict
from typing import Optional, List

@dataclass
class Record:
    """Represents a scraped record from Wikipedia."""

    id: str
    title: str
    site_url: str
    page_url: str
    content: Optional[str] = None
    published_at: Optional[str] = None
    categories: List[str] = None
    scraped_at: str = ""

    def to_dict(self) -> dict:
        """Serialize the Record into a dictionary using asdict for efficiency."""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "Record":
        """Deserialize a dictionary into a Record instance."""
        return cls(**data)