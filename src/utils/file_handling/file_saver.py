import os
import csv

from src.utils.logging.logger_setup import setup_logger

logger = setup_logger()

output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', 'output'))

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

def save_to_text(brand, product, file_name):
    """Сохраняет данные в текстовый файл."""
    if brand and product:
        file_path = os.path.join(output_dir, f"{file_name}.txt")
        try:
            with open(file_path, 'a', encoding='utf-8') as file:
                file.write(f"{brand} | {product}\n")
            logger.info(f"Данные сохранены в файл {file_path}")
        except Exception as e:
            logger.error(f"Ошибка при записи в файл {file_path}: {e}")
    else:
        logger.warning(f"Некорректные данные: Brand - {brand}, Product - {product}")

def save_to_csv(brand, product, file_name):
    """Сохраняет данные в CSV-файл."""
    if brand and product:
        file_path = os.path.join(output_dir, f"{file_name}.csv")
        try:
            with open(file_path, 'a', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                if file.tell() == 0:
                    writer.writerow(["Brand", "Product"])
                writer.writerow([brand, product])
            logger.info(f"Данные сохранены в файл {file_path}")
        except Exception as e:
            logger.error(f"Ошибка при записи в файл {file_path}: {e}")
    else:
        logger.warning(f"Некорректные данные: Brand - {brand}, Product - {product}")