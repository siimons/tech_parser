import re
import math

import requests 
from bs4 import BeautifulSoup

from src.utils.logging.logger_setup import setup_logger
from src.utils.file_handling.file_saver import save_to_csv

logger = setup_logger(log_file='pzip_parser.log')

def get_total_pages(total_info):
    """
    Функция извлекает количество товаров на странице и общее количество товаров, 
    и рассчитывает общее количество страниц.

    :param total_info: строка с информацией о товарах (например, 'Показано товаров: 10 из 460')
    :return: total_pages (общее количество страниц)
    """
    match = re.search(r'Показано товаров: (\d+) из (\d+)', total_info)
    if match:
        items_per_page = int(match.group(1))
        total_items = int(match.group(2))
        total_pages = math.ceil(total_items / items_per_page)
        return total_pages
    else:
        logger.error('Не удалось извлечь информацию о товарах со страницы.')
        return None

def parse_pzip():
    url = 'https://pzip.ru/brands/'
    
    try:
        response = requests.get(url)
        logger.debug(response.status_code)
        
        html = response.text
        soup = BeautifulSoup(html, 'lxml')
        
        producers = soup.find_all('div', class_='col-lg-2 col-md-3 col-sm-4 col-xs-6')
        
        for producer in producers:
            ref_product_catalog = producer.find('a')['href']
            response = requests.get(ref_product_catalog)
            html = response.text
            soup = BeautifulSoup(html, 'lxml')
            
            product_catalog = soup.find_all('li', class_='li-cat-with-image')
            
            for product_type in product_catalog:
                ref_product = product_type.find('a')['href']
                response = requests.get(ref_product)
                html = response.text 
                soup = BeautifulSoup(html, 'lxml')
                
                item_catalog = soup.find_all('li', class_='li-cat-with-image')

                for item_type in item_catalog:
                    ref_item_type = item_type.find('a')['href']
                    
                    response = requests.get(ref_item_type)
                    html = response.text
                    soup = BeautifulSoup(html, 'lxml')
                    
                    total_info = soup.find('div', class_='prod-num-info').text.strip()
                    
                    total_pages = get_total_pages(total_info)
                    
                    if total_pages is None:
                        continue

                    # Цикл для обхода всех страниц товаров
                    for page_num in range(1, total_pages + 1):
                        page_url = f"{ref_item_type}?pg={page_num}"
                        response = requests.get(page_url)
                        html = response.text
                        soup = BeautifulSoup(html, 'lxml')
                        
                        items = soup.find_all('div', class_='product-thumb col-lg-2 col-md-3 col-sm-3 col-xs-4')
                        
                        for item in items:
                            ref_item = item.find('a')['href']
                            response = requests.get(ref_item)
                            html = response.text
                            soup = BeautifulSoup(html, 'lxml')
                            
                            brand = soup.find('h1', class_='product-heading').find('span', id='pbrnd', itemprop='name')
                            brand_name = brand.text.strip()
                            
                            product = soup.find('h1', class_='product-heading').find('span', id='pttl', itemprop='name')
                            product_name = product.text.strip()
                        
                            logger.debug(f'{brand_name} | {product_name}')
                            save_to_csv(brand_name, product_name, 'pzip')
                            
    except requests.RequestException as e:
        logger.error(f'Ошибка при запросе основной страницы {url}: {e}')
