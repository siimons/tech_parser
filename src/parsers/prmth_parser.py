import requests
from bs4 import BeautifulSoup

from src.utils.http_client import create_session, fetch_page
from src.utils.data_saver import save_to_csv

from src.utils.logging import logger


def parse_brand_page(url: str, session: requests.Session) -> None:
    """Парсит страницу бренда и извлекает данные о продуктах.

    Args:
        url (str): URL страницы бренда.
        session (requests.Session): Сессия для выполнения запросов.
    """
    try:
        html = fetch_page(url, session)
        soup = BeautifulSoup(html, "lxml")

        details = soup.find_all("div", class_="products-col")

        for detail in details:
            title_tag = detail.find("a", class_="products-item__title", target="_blank")
            
            if title_tag:
                full_text = title_tag.text.strip()
                parts = full_text.split(maxsplit=1)
                brand = parts[0]
                product = parts[1] if len(parts) > 1 else None
            else:
                brand = None
                product = None

            if brand and product:
                logger.info(f"{brand} | {product}")
                save_to_csv(brand, product, "prmth")

    except Exception as e:
        logger.error(f"Ошибка при парсинге страницы бренда {url}: {e}")


def run_prmth_parser() -> None:
    """Основная функция для парсинга сайта prmth.ru."""
    url = "https://prmth.ru/info/117/"
    session = create_session()

    try:
        html = fetch_page(url, session)
        soup = BeautifulSoup(html, "lxml")

        links = soup.find_all("div", class_="brands_item")

        for link in links:
            ref_label = "https://prmth.ru/" + link.find("a")["href"]
            parse_brand_page(ref_label, session)

    except Exception as e:
        logger.error(f"Ошибка при парсинге основной страницы {url}: {e}")
