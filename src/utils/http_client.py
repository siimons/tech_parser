import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from src.utils.logging import logger


def create_session() -> requests.Session:
    """Создает и настраивает сессию для HTTP-запросов.

    Returns:
        requests.Session: Настроенная сессия.
    """
    session = requests.Session()
    retry = Retry(
        total=3,
        backoff_factor=1,
        status_forcelist=[500, 502, 503, 504],
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    return session


def fetch_page(url: str, session: requests.Session) -> str:
    """Выполняет HTTP-запрос и возвращает HTML-код страницы.

    Args:
        url (str): URL страницы.
        session (requests.Session): Сессия для выполнения запросов.

    Returns:
        str: HTML-код страницы.

    Raises:
        requests.RequestException: Если запрос завершился ошибкой.
    """
    try:
        response = session.get(url, verify=False)
        response.raise_for_status()
        # logger.info(f"Успешный запрос: {url}, статус: {response.status_code}")
        return response.text
    except requests.RequestException as e:
        logger.error(f"Ошибка при запросе страницы {url}: {e}")
        raise