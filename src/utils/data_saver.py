import os
import csv
from typing import Optional

from src.utils.logging import logger

output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "data"))
os.makedirs(output_dir, exist_ok=True)


def save_to_text(brand: Optional[str], product: Optional[str], file_name: str) -> None:
    """Сохраняет данные в текстовый файл."""
    if not brand or not product:
        logger.warning(f"Некорректные данные: Brand - {brand}, Product - {product}")
        return

    file_path = os.path.join(output_dir, f"{file_name}.txt")
    try:
        with open(file_path, "a", encoding="utf-8") as file:
            file.write(f"{brand} | {product}\n")
        logger.info(f"Данные сохранены в файл {file_path}")
    except Exception as e:
        logger.error(f"Ошибка при записи в файл {file_path}: {e}")


def save_to_csv(brand: Optional[str], product: Optional[str], file_name: str) -> None:
    """Сохраняет данные в CSV-файл."""
    if not brand or not product:
        logger.warning(f"Некорректные данные: Brand - {brand}, Product - {product}")
        return

    file_path = os.path.join(output_dir, f"{file_name}.csv")
    try:
        with open(file_path, "a", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            if file.tell() == 0:
                writer.writerow(["Brand", "Product"])
            writer.writerow([brand, product])
        logger.info(f"Данные сохранены в файл {file_path}")
    except Exception as e:
        logger.error(f"Ошибка при записи в файл {file_path}: {e}")
