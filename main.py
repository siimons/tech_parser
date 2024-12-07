from concurrent.futures import ThreadPoolExecutor, as_completed

from src.parsers.ei_spb_parser import parse_ei_spb
from src.parsers.prmth_parser import parse_prmth
from src.parsers.pzip_parser import parse_pzip
from src.parsers.dalkos_parser import parse_dalkos

from src.utils.logging.logger_setup import setup_logger

logger = setup_logger(log_file='parser.log')

def execute_parsers(parsers):
    """
    Запускает парсеры в пуле потоков и логирует результаты их выполнения.
    
    :param parsers: Список функций-парсеров.
    """
    with ThreadPoolExecutor(max_workers=len(parsers)) as executor:
        future_to_parser = {executor.submit(parser): parser.__name__ for parser in parsers}

        for future in as_completed(future_to_parser):
            parser_name = future_to_parser[future]
            try:
                result = future.result()
                logger.info(f"Парсер {parser_name} успешно завершил работу.")
            except Exception as e:
                logger.error(f"Ошибка в парсере {parser_name}: {e}")

def main():
    """
    Основная функция для запуска программы.
    """
    parsers = [
        parse_ei_spb,
        parse_prmth,
        parse_pzip,
        parse_dalkos
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