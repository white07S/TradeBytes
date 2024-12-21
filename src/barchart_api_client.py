import requests
import json
import logging
from typing import Any, Dict, List
from src.barchart_session_manager import SessionManager
from pydantic import BaseModel, ValidationError

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class APIQueryParams(BaseModel):
    orderBy: str
    orderDir: str
    fields: List[str]

class APIConfig(BaseModel):
    base_api_url: str
    query_params: APIQueryParams

class ConfigModel(BaseModel):
    common: Dict[str, Any]
    apis: Dict[str, APIConfig]

class APIClient:
    def __init__(self, config_path: str, main_url: str = "https://www.barchart.com/"):
        self.main_url = main_url
        self.config = self.load_config(config_path)
        self.common_headers = self.config.common['headers']
        self.dynamic_headers = self.config.common['dynamic_headers']
        self.base_api_params = self.config.common['base_api_params']
        self.max_pages = self.config.common.get('max_pages', 10)
        self.apis = self.config.apis
        self.session_manager = SessionManager(main_url=self.main_url, common_headers=self.common_headers)

    @staticmethod
    def load_config(config_path: str) -> ConfigModel:
        try:
            with open(config_path, 'r') as f:
                config_dict = json.load(f)
            config = ConfigModel(**config_dict)
            logger.info(f"Configuration loaded and validated from {config_path}.")
            return config
        except ValidationError as ve:
            logger.exception(f"Configuration validation error: {ve}")
            raise
        except Exception as e:
            logger.exception(f"Failed to load configuration: {e}")
            raise

    def fetch_api_data(self, api_name: str) -> Dict[str, Any]:
        if api_name not in self.apis:
            logger.error(f"API '{api_name}' not found in configuration.")
            raise ValueError(f"API '{api_name}' not found in configuration.")

        api_config = self.apis[api_name]
        base_api_url = api_config.base_api_url
        query_params = api_config.query_params.dict()

        # Convert list parameters to comma-separated strings
        for key, value in query_params.items():
            if isinstance(value, list):
                query_params[key] = ",".join(value)

        query_params.update(self.base_api_params)

        try:
            session, csrf_token = self.session_manager.get_session_and_token()
            headers = self.common_headers.copy()

            # Update dynamic headers
            headers.update({
                'User-Agent': self.session_manager.ua.random,
                'Referer': self.main_url,
                'X-CSRF-TOKEN': csrf_token
            })

            all_data: List[Dict[str, Any]] = []
            current_page = 1
            total_records = 0

            while current_page <= self.max_pages:
                query_params['page'] = current_page
                logger.info(f"Fetching page {current_page} from API '{api_name}'.")
                response = session.get(base_api_url, headers=headers, params=query_params)
                response.raise_for_status()
                response_data = response.json()

                if current_page == 1:
                    total_records = response_data.get("total", 0)
                    logger.info(f"Total records available: {total_records}")

                page_data = response_data.get("data", [])
                all_data.extend(page_data)
                logger.info(f"Page {current_page} fetched: {len(page_data)} records. Total fetched: {len(all_data)}")

                if not page_data:
                    logger.info("No more data to fetch.")
                    break

                current_page += 1

            if current_page > self.max_pages:
                logger.info(f"Reached maximum page limit of {self.max_pages}.")

            return {
                "total": total_records,
                "data": all_data
            }

        except requests.RequestException as e:
            logger.exception(f"HTTP error occurred while fetching API '{api_name}': {e}")
            raise
        except Exception as e:
            logger.exception(f"Error occurred while fetching API '{api_name}': {e}")
            raise

    def save_data_to_json(self, data: Dict[str, Any], filename: str) -> None:
        try:
            with open(filename, 'w') as json_file:
                json.dump(data, json_file, indent=4)
            logger.info(f"Data saved successfully to '{filename}'.")
        except Exception as e:
            logger.exception(f"Failed to save data to '{filename}': {e}")
            raise