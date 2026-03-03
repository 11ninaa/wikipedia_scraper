from pydantic_settings import BaseSettings

class ScraperSettings(BaseSettings):
    # Logging
    log_level: str = "INFO"
    log_format: str = "%(asctime)s %(levelname)s %(name)s | %(message)s"
    log_to_file: bool = True
    log_file_path: str = "logs/scraper.log"

    # Site details
    site_url: str = "https://mk.wikipedia.org/w/api.php"
    site_name: str = "macedonian_wikipedia"
    root_category: str = "Македонија"

    # Scraping Limits
    max_depth: int = 5
    max_articles: int = 10000

    # Scraping settings
    max_concurrent_requests: int = 1
    request_timeout: int = 30

    requests_per_second: float = 1.0
    max_retries: int = 3
    retry_delay: float = 10.0
    retry_backoff: float = 2.0

    headers: dict = {
        'User-Agent': 'VezilkaDatasetCollector/1.0 (Language Research Project; contact: research-team@example.com)',
        'Accept': 'application/json'
    }

    model_config = {
        "env_file": ".env",
        "extra": "ignore"
    }

settings = ScraperSettings()