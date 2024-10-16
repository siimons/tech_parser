import os
import asyncio 
import requests
from src.utils.logger_setup import setup_logger

from src.utils.user_agent import get_random_user_agent
from src.utils.proxy_picker import get_random_proxy

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

"""Функционал для сохранения собранной информации в текстовые файлы"""
lock = asyncio.Lock()

output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'output'))

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

async def save_to_text(brand, product, file_name):
    if brand and product:
        file_path = os.path.join(output_dir, f"{file_name}.txt")

        async with lock:
            try:
                with open(file_path, 'a', encoding='utf-8') as file:
                    file.write(f"{brand} | {product}\n")
                logger.info(f"Данные сохранены в файл {file_path}")
            except Exception as e:
                logger.error(f"Ошибка при записи в файл {file_path}: {e}")
    else:
        logger.warning(f"Некорректные данные: Brand - {brand}, Product - {product}")