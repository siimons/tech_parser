from concurrent.futures import ThreadPoolExecutor, as_completed

from src.parsers.dalkos_parser import run_dalkos_parser
from src.parsers.ei_spb_parser import run_ei_spb_parser
from src.parsers.prmth_parser import run_prmth_parser
from src.parsers.pzip_parser import run_pzip_parser

from src.utils.logging import logger


def execute_parsers(parsers):
    with ThreadPoolExecutor(max_workers=4) as executor:
        future_to_parser = {
            executor.submit(parser): parser.__name__ for parser in parsers
        }

        for future in as_completed(future_to_parser):
            parser_name = future_to_parser[future]
            try:
                future.result()
                logger.info(f"Парсер {parser_name} успешно завершил работу.")
            except Exception as e:
                logger.error(f"Ошибка в парсере {parser_name}: {e}")


def main():
    parsers = [
        run_dalkos_parser,
        run_ei_spb_parser,
        run_prmth_parser,
        run_pzip_parser,
    ]

    logger.info("Запуск парсеров.")
    try:
        execute_parsers(parsers)
    except KeyboardInterrupt:
        logger.warning("Прерывание программы! Завершаем выполнение парсеров...")
    except Exception as e:
        logger.error(f"Критическая ошибка во время выполнения: {e}")
    finally:
        logger.info("Завершение программы.")


if __name__ == "__main__":
    main()