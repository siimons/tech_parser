import re
import math

import requests
from bs4 import BeautifulSoup

from src.utils.http_client import create_session, fetch_page
from src.utils.data_saver import save_to_csv

from src.utils.logging import logger


def get_total_pages(total_info: str) -> int:
    """Извлекает количество товаров на странице и общее количество товаров, и рассчитывает общее количество страниц.

    Args:
        total_info (str): Строка с информацией о товарах (например, 'Показано товаров: 10 из 460').

    Returns:
        int: Общее количество страниц. Если информация не найдена, возвращает None.
    """
    match = re.search(r"Показано товаров: (\d+) из (\d+)", total_info)
    if match:
        items_per_page = int(match.group(1))
        total_items = int(match.group(2))
        total_pages = math.ceil(total_items / items_per_page)
        return total_pages
    else:
        logger.error("Не удалось извлечь информацию о товарах со страницы.")
        return None


def parse_item_page(url: str, session: requests.Session) -> None:
    """Парсит страницу товара и извлекает данные о бренде и продукте.

    Args:
        url (str): URL страницы товара.
        session (requests.Session): Сессия для выполнения запросов.
    """
    try:
        html = fetch_page(url, session)
        soup = BeautifulSoup(html, "lxml")

        brand = soup.find("h1", class_="product-heading").find("span", id="pbrnd", itemprop="name")
        brand_name = brand.text.strip()

        product = soup.find("h1", class_="product-heading").find("span", id="pttl", itemprop="name")
        product_name = product.text.strip()

        logger.info(f"{brand_name} | {product_name}")
        save_to_csv(brand_name, product_name, "pzip")

    except Exception as e:
        logger.error(f"Ошибка при парсинге страницы товара {url}: {e}")


def parse_item_type_page(url: str, session: requests.Session) -> None:
    """Парсит страницу с типом товара и извлекает данные о товарах.

    Args:
        url (str): URL страницы с типом товара.
        session (requests.Session): Сессия для выполнения запросов.
    """
    try:
        html = fetch_page(url, session)
        soup = BeautifulSoup(html, "lxml")

        total_info = soup.find("div", class_="prod-num-info").text.strip()
        total_pages = get_total_pages(total_info)

        if total_pages is None:
            return

        for page_num in range(1, total_pages + 1):
            page_url = f"{url}?pg={page_num}"
            html = fetch_page(page_url, session)
            soup = BeautifulSoup(html, "lxml")

            items = soup.find_all("div", class_="product-thumb col-lg-2 col-md-3 col-sm-3 col-xs-4")

            for item in items:
                ref_item = item.find("a")["href"]
                parse_item_page(ref_item, session)

    except Exception as e:
        logger.error(f"Ошибка при парсинге страницы типа товара {url}: {e}")


def parse_product_catalog(url: str, session: requests.Session) -> None:
    """Парсит каталог продуктов и извлекает данные о типах товаров.

    Args:
        url (str): URL каталога продуктов.
        session (requests.Session): Сессия для выполнения запросов.
    """
    try:
        html = fetch_page(url, session)
        soup = BeautifulSoup(html, "lxml")

        product_catalog = soup.find_all("li", class_="li-cat-with-image")

        for product_type in product_catalog:
            ref_product = product_type.find("a")["href"]
            parse_item_type_page(ref_product, session)

    except Exception as e:
        logger.error(f"Ошибка при парсинге каталога продуктов {url}: {e}")


def parse_producer_page(url: str, session: requests.Session) -> None:
    """Парсит страницу производителя и извлекает данные о каталогах продуктов.

    Args:
        url (str): URL страницы производителя.
        session (requests.Session): Сессия для выполнения запросов.
    """
    try:
        html = fetch_page(url, session)
        soup = BeautifulSoup(html, "lxml")

        producers = soup.find_all("div", class_="col-lg-2 col-md-3 col-sm-4 col-xs-6")

        for producer in producers:
            ref_product_catalog = producer.find("a")["href"]
            parse_product_catalog(ref_product_catalog, session)

    except Exception as e:
        logger.error(f"Ошибка при парсинге страницы производителя {url}: {e}")


def run_pzip_parser() -> None:
    """Основная функция для запуска парсера сайта pzip.ru."""
    url = "https://pzip.ru/brands/"
    session = create_session()

    try:
        parse_producer_page(url, session)
    except Exception as e:
        logger.error(f"Ошибка при парсинге основной страницы {url}: {e}")
