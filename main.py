import asyncio
from concurrent.futures import ThreadPoolExecutor

from src.utils.file_utils import setup_logger

from src.parsers.ei_spb_parser import parse_ei_spb
from src.parsers.prmth_parser import parse_prmth
from src.parsers.pzip_async_parser import parse_pzip
from src.parsers.dalkos_async_parser import parse_dalkos

logger = setup_logger(log_file='parser.log')

async def main():
    tasks = [
        asyncio.create_task(parse_pzip()),
        asyncio.create_task(parse_dalkos())
    ]

    with ThreadPoolExecutor() as executor:
        tasks.append(asyncio.get_event_loop().run_in_executor(executor, parse_ei_spb))
        tasks.append(asyncio.get_event_loop().run_in_executor(executor, parse_prmth))

    try:
        await asyncio.gather(*tasks)
    except asyncio.CancelledError:
        logger.warning("Задачи отменены.")
    except Exception as e:
        logger.error(f"Произошла ошибка: {e}")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.warning("Программа была прервана пользователем.")
