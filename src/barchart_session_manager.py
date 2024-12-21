import requests
from bs4 import BeautifulSoup
import re
import logging
from fake_useragent import UserAgent
from typing import Tuple, Dict

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SessionManager:
    def __init__(self, main_url: str, common_headers: Dict[str, str]):
        self.main_url = main_url
        self.ua = UserAgent()
        self.common_headers = common_headers

    def create_session(self) -> requests.Session:
        session = requests.Session()
        logger.info("Session created.")
        return session

    def fetch_csrf_token(self, session: requests.Session) -> str:
        headers = self.common_headers.copy()
        headers.update({
            'User-Agent': self.ua.random,
            'Referer': self.main_url
        })

        try:
            response = session.get(self.main_url, headers=headers)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            csrf_token = None

            # Attempt to find CSRF token in meta tags
            meta = soup.find('meta', {'name': 'csrf-token'})
            if meta:
                csrf_token = meta.get('content')
                logger.debug("CSRF token found in meta tag.")
            else:
                # Alternative: Look for CSRF token in JavaScript variables
                scripts = soup.find_all('script')
                for script in scripts:
                    if script.string and 'csrf' in script.string.lower():
                        match = re.search(r'csrfToken\s*:\s*"([^"]+)"', script.string, re.IGNORECASE)
                        if match:
                            csrf_token = match.group(1)
                            logger.debug("CSRF token found in JavaScript.")
                            break

            if not csrf_token:
                logger.error("CSRF token not found.")
                raise ValueError("CSRF token not found")

            logger.info("CSRF token retrieved successfully.")
            return csrf_token

        except requests.RequestException as e:
            logger.exception(f"HTTP error occurred while fetching CSRF token: {e}")
            raise
        except Exception as e:
            logger.exception(f"Error occurred while fetching CSRF token: {e}")
            raise

    def get_session_and_token(self) -> Tuple[requests.Session, str]:
        session = self.create_session()
        csrf_token = self.fetch_csrf_token(session)
        return session, csrf_token