import requests
from bs4 import BeautifulSoup

from src.utils.logger_setup import setup_logger
from src.utils.file_utils import save_to_csv, save_to_text

logger = setup_logger(log_file='ei_spb_parser.log')

def parse_ei_spb():
    try:
        url = 'https://ei.spb.ru/brands'
        response = requests.get(url)
        html = response.text
        soup = BeautifulSoup(html, 'lxml')
        
        page_count = int(soup.find_all('a', class_='page-link')[-2].text)
        
        for i in range(1, page_count):
            url = f'https://ei.spb.ru/brands?page={i}'
            response = requests.get(url)
            logger.debug(f"Статус-код страницы {i}: {response.status_code}")

            if response.status_code == 200:
                html = response.text
                soup = BeautifulSoup(html, 'lxml')

                links = soup.find_all(class_='col mb-4')

                for link in links:
                    ref_label = link.find('a')['href']
                    # logger.debug(f"Найдена ссылка на бренд: {ref_label}")

                    response = requests.get(ref_label)
                    # logger.debug(f"Статус-код страницы бренда: {response.status_code}")

                    if response.status_code == 200:
                        html = response.text
                        soup = BeautifulSoup(html, 'lxml')

                        brand_name_tag = soup.find('h1')
                        brand_name = brand_name_tag.text.strip() if brand_name_tag else "Без названия"

                        elements = soup.find_all('div', class_='col-md-6 col-lg-4 mb-4')

                        for element in elements:
                            element_title = element.find('h2', class_='h5 text-black').find('a')
                            product_name = element_title.get_text(strip=True) if element_title else None

                            logger.info(f"{brand_name} | {product_name}")
                            save_to_csv(brand_name, product_name, 'ei_spb')

                    else:
                        logger.warning(f"Не удалось получить данные со страницы бренда: {ref_label}, статус-код: {response.status_code}")

            else:
                logger.error(f"Не удалось получить доступ к странице {url}, статус-код: {response.status_code}")

    except Exception as e:
        logger.exception(f"Ошибка во время парсинга: {e}")
