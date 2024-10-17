from concurrent.futures import ThreadPoolExecutor

from src.utils.file_utils import setup_logger

from src.parsers.ei_spb_parser import parse_ei_spb
from src.parsers.prmth_parser import parse_prmth
from src.parsers.pzip_parser import parse_pzip
from src.parsers.dalkos_parser import parse_dalkos

logger = setup_logger(log_file='parser.log')

def main():
    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = [
            executor.submit(parse_pzip),
            executor.submit(parse_dalkos),
            executor.submit(parse_ei_spb),
            executor.submit(parse_prmth)
        ]
        
        for future in futures:
            try:
                future.result()
            except Exception as e:
                logger.error(f"Произошла ошибка при выполнении задачи: {e}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.warning("Программа была прервана пользователем.")