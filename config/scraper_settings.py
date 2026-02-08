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

    # Rate limiting
    requests_per_second: float = 1.0

    # Retry settings
    max_retries: int = 3
    retry_delay: float = 1.0
    retry_backoff: float = 2.0

    headers: dict = {
        'User-Agent': 'MacedonianResearchBot/1.0 (Educational purpose; contact: research@example.com)',
        'Accept': 'application/json'
    }

    model_config = {
        "env_file": ".env",
        "extra": "ignore"
    }

settings = ScraperSettings()