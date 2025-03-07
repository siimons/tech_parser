import requests
from bs4 import BeautifulSoup

from src.utils.http_client import create_session, fetch_page
from src.utils.data_saver import save_to_csv

from src.utils.logging import logger


def get_page_count(soup: BeautifulSoup) -> int:
    """Извлекает количество страниц с брендами.

    Args:
        soup (BeautifulSoup): Объект BeautifulSoup для парсинга HTML.

    Returns:
        int: Количество страниц.
    """
    page_links = soup.find_all("a", class_="page-link")
    return int(page_links[-2].text) if page_links else 1


def parse_brand_page(url: str, session: requests.Session) -> None:
    """Парсит страницу бренда и извлекает данные о продуктах.

    Args:
        url (str): URL страницы бренда.
        session (requests.Session): Сессия для выполнения запросов.
    """
    try:
        html = fetch_page(url, session)
        soup = BeautifulSoup(html, "lxml")

        brand_name_tag = soup.find("h1")
        brand_name = brand_name_tag.text.strip() if brand_name_tag else "Без названия"

        elements = soup.find_all("div", class_="col-md-6 col-lg-4 mb-4")

        for element in elements:
            element_title = element.find("h2", class_="h5 text-black").find("a")
            product_name = element_title.get_text(strip=True) if element_title else None

            if product_name:
                logger.info(f"{brand_name} | {product_name}")
                save_to_csv(brand_name, product_name, "ei_spb")

    except Exception as e:
        logger.error(f"Ошибка при парсинге страницы бренда {url}: {e}")


def parse_page(url: str, session: requests.Session) -> None:
    """Парсит страницу с брендами и извлекает ссылки на страницы брендов.

    Args:
        url (str): URL страницы с брендами.
        session (requests.Session): Сессия для выполнения запросов.
    """
    try:
        html = fetch_page(url, session)
        soup = BeautifulSoup(html, "lxml")

        links = soup.find_all(class_="col mb-4")

        for link in links:
            ref_label = link.find("a")["href"]
            parse_brand_page(ref_label, session)

    except Exception as e:
        logger.error(f"Ошибка при парсинге страницы {url}: {e}")


def run_ei_spb_parser() -> None:
    """Основная функция для запуска парсера сайта ei.spb.ru."""
    try:
        base_url = "https://ei.spb.ru/brands"
        session = create_session()

        html = fetch_page(base_url, session)
        soup = BeautifulSoup(html, "lxml")
        page_count = get_page_count(soup)

        for page_num in range(1, page_count + 1):
            url = f"{base_url}?page={page_num}"
            # logger.info(f"Парсинг страницы {page_num} из {page_count}")
            parse_page(url, session)

    except Exception as e:
        logger.exception(f"Ошибка во время парсинга: {e}")
