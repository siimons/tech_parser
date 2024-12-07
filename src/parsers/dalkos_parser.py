import requests 
from bs4 import BeautifulSoup

from src.utils.logging.logger_setup import setup_logger
from src.utils.file_handling.file_saver import save_to_csv

logger = setup_logger(log_file='dalkos_parser.log')

def parse_dalkos():
    url = 'https://dalkos.ru/catalog/'
    
    try:
        response = requests.get(url, verify=False)
        logger.debug(response.status_code)
        
        html = response.text
        soup = BeautifulSoup(html, 'lxml')
        
        equipment_catalog = soup.find_all('div', class_='categoreProduct__row__item__text')
        
        for equipment_type in equipment_catalog:
            ref_equipment = equipment_type.find('a')['href']
            response = requests.get(url=f'https://dalkos.ru{ref_equipment}', verify=False)
            html = response.text
            soup = BeautifulSoup(html, 'lxml')
            
            equipments = soup.find_all('div', class_='categoreProduct__row__item')
            
            for equipment in equipments:
                ref_brand = equipment.find('a')['href']
                response = requests.get(url=f'https://dalkos.ru{ref_brand}', verify=False)
                html = response.text
                soup = BeautifulSoup(html, 'lxml')
                
                brands_equipment = soup.find_all('div', class_='categoreProduct__row__item')
                brand_name = soup.find('div', class_='categoreProduct__row__item__text').text.strip()
                
                for brand in brands_equipment:
                    ref_product = brand.find('a')['href']
                    response = requests.get(url=f'https://dalkos.ru{ref_product}', verify=False)
                    html = response.text
                    soup = BeautifulSoup(html, 'lxml')
                    
                    products = soup.find_all('div', class_='favoriteProduct__row__item__text')
                    
                    for product in products:
                        product_name = product.find('a').text.strip()
            
                        logger.debug(f'{brand_name} | {product_name}')
                        save_to_csv(brand_name, product_name, 'dalkos')
                        
    except requests.RequestException as e:
        logger.error(f'Ошибка при запросе основной страницы {url}: {e}')
