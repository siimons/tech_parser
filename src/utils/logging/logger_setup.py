import os
from loguru import logger

def setup_logger(log_dir='logs', log_file='parser.log', level='INFO'):
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    log_file_path = os.path.join(log_dir, log_file)
    logger.add(log_file_path, format="{time} {level} {message}", level=level)
    
    return logger
