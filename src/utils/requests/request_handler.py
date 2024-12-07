import requests

from src.utils.requests.user_agent import get_random_user_agent
from src.utils.requests.proxy_picker import get_random_proxy

from src.utils.logging.logger_setup import setup_logger

logger = setup_logger()

def create_request(url):
    """Создает HTTP-запрос с случайным User-Agent и прокси."""
    user_agent = get_random_user_agent()
    proxy = get_random_proxy()

    headers = {
        'User-Agent': user_agent
    }

    proxy_dict = {
        "http": proxy,
        "https": proxy,
    }

    try:
        response = requests.get(url, headers=headers, proxies=proxy_dict)
        response.raise_for_status()
        return response
    except requests.exceptions.RequestException as e:
        logger.error(f"Ошибка при запросе: {e}")
        return None
