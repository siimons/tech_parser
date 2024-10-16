import requests
from bs4 import BeautifulSoup

from src.utils.logger_setup import setup_logger
from src.utils.file_utils import save_to_text

logger = setup_logger(log_file='prmth_parser.log')

def parse_prmth():
    url = 'https://prmth.ru/info/117/'

    try:
        response = requests.get(url)
        response.raise_for_status()

        logger.debug(f"Статус-код основной страницы: {response.status_code}")

        html = response.text
        soup = BeautifulSoup(html, 'lxml')

        # Находим все ссылки на бренды
        links = soup.find_all('div', class_='brands_item')

        for link in links:
            try:
                ref_label = 'https://prmth.ru/' + link.find('a')['href']
                # logger.debug(f"Найдена ссылка на бренд: {ref_label}")

                # Запрос к странице бренда
                response = requests.get(ref_label)
                response.raise_for_status()

                # logger.debug(f"Статус-код страницы бренда: {response.status_code}")

                html = response.text
                soup = BeautifulSoup(html, 'lxml')

                # Находим все товары на странице бренда
                details = soup.find_all('div', class_='products-col')

                for detail in details:
                    title_tag = detail.find('a', class_='products-item__title', target='_blank')
                    
                    if title_tag:
                        full_text = title_tag.text.strip()
                        parts = full_text.split(maxsplit=1)
                        brand = parts[0]
                        product = parts[1] if len(parts) > 1 else None
                    else:
                        brand = None
                        product = None

                    logger.info(f"{brand} | {product}")
                    save_to_text(brand, product, 'prmth')

            except requests.RequestException as e:
                logger.error(f"Ошибка при запросе страницы бренда {ref_label}: {e}")

    except requests.RequestException as e:
        logger.error(f"Ошибка при запросе основной страницы {url}: {e}")

# if __name__ == '__main__':
#     parse_prmth()