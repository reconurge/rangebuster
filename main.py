import os
import multiprocessing
import argparse
import time
from loguru import logger
from common.utils import get_duration
from common.config import CACHE_PATH, sources
from packages.rir_connector import RiRConnector
from packages.arin_connector import ArinConnector

# Logger setup
logger.remove()  # Remove the default configuration (file handler)
logger.add(lambda msg: print(msg, end=''), colorize=True, format="<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level: <8}</level> | <level>{message}</level>", level="INFO", diagnose=False)

def main():
    processes = []
    os.makedirs(CACHE_PATH, exist_ok=True)

    parser = argparse.ArgumentParser(
        prog="cidr_recon",
        description="Search RR/RIR database for keywords."
    )
    parser.add_argument(
        "keywords", help="Keywords to search for. Separate multiple keywords with commas."
    )
    parser.add_argument("-s", "--strict", action="store_true", help="Perform strict keyword matching.")
    parser.add_argument("-nc", "--no_cache", action="store_true", help="Clear the cache folder (where databases are stored).")
    parser.add_argument('-o', '--output', type=str, default=None, help='Output filename (should end with .json)')

    arg = parser.parse_args()

    if arg.no_cache:
        try:
            os.remove(CACHE_PATH)
        except PermissionError:
            logger.warning(f"Permission denied: Unable to remove {CACHE_PATH}.")
            logger.warning("If you want to clear the cache, please run the script with elevated permissions (e.g., using 'sudo').")
        except IsADirectoryError:
            logger.warning(f"{CACHE_PATH} is a directory. Use 'shutil.rmtree()' to remove directories.")
        except FileNotFoundError:
            logger.warning(f"Cache path {CACHE_PATH} does not exist.")
        except Exception as e:
            logger.warning(f"An error occurred while trying to remove the cache: {e}")
        
    if arg.strict:
            logger.info("Using strict mode.")

    download_processes = []
    for section in sources:
        name = section['name']
        url = section['url']
        db_file = section['db_file']
        rir_connector = RiRConnector(output_file=arg.output, keywords=arg.keywords, strict=arg.strict, source=name, db_file=db_file)
        process = multiprocessing.Process(target=rir_connector.download_database, args=(url, os.path.join(CACHE_PATH, db_file)))
        download_processes.append(process)

    # Start the download processes
    for process in download_processes:
        process.start()
    for process in download_processes:
        process.join()

    # Search databases after downloading
    for section in sources:
        name = section['name']
        db_file = section['db_file']
        rir_connector = RiRConnector(output_file=arg.output, keywords=arg.keywords, strict=arg.strict, source=name, db_file=db_file)
        process = multiprocessing.Process(target=rir_connector.run)
        processes.append(process)

    for process in processes:
        process.start()
    for process in processes:
        process.join()

if __name__ == "__main__":
    start_time = time.time()
    main()
    end_time = time.time()
    finished = get_duration(start_time, end_time)
    logger.success(f"Finished in {finished}")
