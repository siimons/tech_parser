import requests
from bs4 import BeautifulSoup

from src.utils.http_client import create_session, fetch_page
from src.utils.data_saver import save_to_csv

from src.utils.logging import logger


def parse_equipment_catalog(url: str, session: requests.Session) -> None:
    """Парсит каталог оборудования и извлекает данные о брендах и продуктах.

    Args:
        url (str): URL каталога оборудования.
        session (requests.Session): Сессия для выполнения запросов.
    """
    try:
        html = fetch_page(url, session)
        soup = BeautifulSoup(html, "lxml")

        equipment_catalog = soup.find_all("div", class_="categoreProduct__row__item__text")

        for equipment_type in equipment_catalog:
            ref_equipment = equipment_type.find("a")["href"]
            parse_equipment_type(f"https://dalkos.ru{ref_equipment}", session)

    except Exception as e:
        logger.error(f"Ошибка при парсинге каталога оборудования: {e}")


def parse_equipment_type(url: str, session: requests.Session) -> None:
    """Парсит страницу с конкретным типом оборудования и извлекает данные о брендах.

    Args:
        url (str): URL страницы с типом оборудования.
        session (requests.Session): Сессия для выполнения запросов.
    """
    try:
        html = fetch_page(url, session)
        soup = BeautifulSoup(html, "lxml")

        equipments = soup.find_all("div", class_="categoreProduct__row__item")

        for equipment in equipments:
            ref_brand = equipment.find("a")["href"]
            parse_brand(f"https://dalkos.ru{ref_brand}", session)

    except Exception as e:
        logger.error(f"Ошибка при парсинге типа оборудования: {e}")


def parse_brand(url: str, session: requests.Session) -> None:
    """Парсит страницу бренда и извлекает данные о продуктах.

    Args:
        url (str): URL страницы бренда.
        session (requests.Session): Сессия для выполнения запросов.
    """
    try:
        html = fetch_page(url, session)
        soup = BeautifulSoup(html, "lxml")

        brands_equipment = soup.find_all("div", class_="categoreProduct__row__item")
        brand_name = soup.find("div", class_="categoreProduct__row__item__text").text.strip()

        for brand in brands_equipment:
            ref_product = brand.find("a")["href"]
            parse_product(f"https://dalkos.ru{ref_product}", brand_name, session)

    except Exception as e:
        logger.error(f"Ошибка при парсинге бренда: {e}")


def parse_product(url: str, brand_name: str, session: requests.Session) -> None:
    """Парсит страницу продукта и сохраняет данные в CSV.

    Args:
        url (str): URL страницы продукта.
        brand_name (str): Название бренда.
        session (requests.Session): Сессия для выполнения запросов.
    """
    try:
        html = fetch_page(url, session)
        soup = BeautifulSoup(html, "lxml")

        products = soup.find_all("div", class_="favoriteProduct__row__item__text")

        for product in products:
            product_name = product.find("a").text.strip()
            logger.info(f"{brand_name} | {product_name}")
            save_to_csv(brand_name, product_name, "dalkos")

    except Exception as e:
        logger.error(f"Ошибка при парсинге продукта: {e}")


def run_dalkos_parser() -> None:
    """Основная функция для запуска парсера сайта dalkos.ru."""
    url = "https://dalkos.ru/catalog/"
    session = create_session()
    parse_equipment_catalog(url, session)
