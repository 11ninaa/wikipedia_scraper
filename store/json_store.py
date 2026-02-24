import json
import logging
from pathlib import Path
from typing import Iterable, List, Dict, Any, Set
from .base_store import BaseStore
from scraper.models import Record

logger = logging.getLogger(__name__)


class JSONFileStore(BaseStore):
    def __init__(self, records_file_path: str, seen_ids_file_path: str):
        self.records_file_path = Path(records_file_path)
        self.seen_ids_file_path = Path(seen_ids_file_path)

        self.records_file_path.parent.mkdir(parents=True, exist_ok=True)
        self.seen_ids_file_path.parent.mkdir(parents=True, exist_ok=True)

        self.seen_ids: Set[str] = self.load_seen_ids()

    def load_all_records(self) -> List[Dict[str, Any]]:
        if not self.records_file_path.exists():
            return []
        try:
            with self.records_file_path.open("r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return []

    def save_records(self, records: Iterable[Record]) -> None:
        records_list = list(records)
        if not records_list:
            return

        existing_records = self.load_all_records()
        for record in records_list:
            existing_records.append(record.to_dict())
            self.seen_ids.add(record.id)

        with self.records_file_path.open("w", encoding="utf-8") as f:
            json.dump(existing_records, f, indent=2, ensure_ascii=False)

        self.save_seen_ids(self.seen_ids)

    def load_seen_ids(self) -> Set[str]:
        if not self.seen_ids_file_path.exists():
            return set()
        try:
            with self.seen_ids_file_path.open("r", encoding="utf-8") as f:
                data = json.load(f)
                return set(data)
        except (json.JSONDecodeError, FileNotFoundError):
            return set()

    def save_seen_ids(self, ids: Set[str]) -> None:
        with self.seen_ids_file_path.open("w", encoding="utf-8") as f:
            json.dump(list(ids), f, indent=2, ensure_ascii=False)

    def clear(self) -> None:
        self.seen_ids.clear()
        if self.records_file_path.exists(): self.records_file_path.unlink()
        if self.seen_ids_file_path.exists(): self.seen_ids_file_path.unlink()