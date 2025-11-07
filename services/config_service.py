import json
from typing import Literal

SortOption = Literal["publish_date", "price"]

class ConfigService:
    def __init__(self, config_path='config.json'):
        self.config_path = config_path
        self._config = self._load_config()

    def _load_config(self) -> dict:
        try:
            with open(self.config_path, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            # If the file doesn't exist or is invalid, create a default config
            default_config = {"book_sort_by": "publish_date"}
            self._save_config(default_config)
            return default_config

    def _save_config(self, config_data: dict):
        with open(self.config_path, 'w') as f:
            json.dump(config_data, f, indent=4)

    def get_book_sort_strategy(self) -> SortOption:
        return self._config.get("book_sort_by", "publish_date")

    def set_book_sort_strategy(self, sort_by: SortOption):
        self._config["book_sort_by"] = sort_by
        self._save_config(self._config)

