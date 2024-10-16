import aiohttp
import asyncio
from bs4 import BeautifulSoup

from src.utils.logger_setup import setup_logger
from src.utils.file_utils import save_to_text

logger = setup_logger(log_file='dalkos_parser.log')

async def get_page(session, url):
    async with session.get(url, ssl=False) as response:
        # logger.debug(response.status)
        return await response.text()

async def parse_dalkos():
    url = 'https://dalkos.ru/catalog/'
    
    try:
        async with aiohttp.ClientSession() as session:
            html = await get_page(session, url)
            soup = BeautifulSoup(html, 'lxml')
            
            equipment_catalog = soup.find_all('div', class_='categoreProduct__row__item__text')
            
            for equipment_type in equipment_catalog:
                ref_equipment = equipment_type.find('a')['href']
                equipment_url = f'https://dalkos.ru{ref_equipment}'
                html = await get_page(session, equipment_url)
                soup = BeautifulSoup(html, 'lxml')
                
                equipments = soup.find_all('div', class_='categoreProduct__row__item')
                
                for equipment in equipments:
                    ref_brand = equipment.find('a')['href']
                    brand_url = f'https://dalkos.ru{ref_brand}'
                    html = await get_page(session, brand_url)
                    soup = BeautifulSoup(html, 'lxml')
                    
                    brands_equipment = soup.find_all('div', class_='categoreProduct__row__item')
                    
                    try:
                        brand_name = soup.find('div', class_='categoreProduct__row__item__text').text.strip()
                    except AttributeError:
                        logger.error(f'Не удалось найти название бренда на странице {brand_url}.')
                        continue
                    
                    for brand in brands_equipment:
                        ref_product = brand.find('a')['href']
                        product_url = f'https://dalkos.ru{ref_product}'
                        html = await get_page(session, product_url)
                        soup = BeautifulSoup(html, 'lxml')
                        
                        products = soup.find_all('div', class_='favoriteProduct__row__item__text')
                        
                        for product in products:
                            product_name = product.find('a').text.strip()
                            logger.info(f'{brand_name} | {product_name}')
                            
                            save_to_text(brand_name, product_name, 'dalkos')
                        
    except aiohttp.ClientError as e:
        logger.error(f'Ошибка при запросе основной страницы {url}: {e}')

# if __name__ == '__main__':
#     asyncio.run(parse_dalkos())