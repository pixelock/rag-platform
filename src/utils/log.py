# coding: utf-8

import os
import logging
from datetime import datetime

from utils.path import LOG_DIR


def get_logger(name=None, level=logging.INFO):
    logger = logging.getLogger(name)
    logger.setLevel(level)

    formatter = logging.Formatter('[%(asctime)s][%(filename)s][%(lineno)d][%(levelname)s] %(message)s')
    file_handler = logging.FileHandler(os.path.join(LOG_DIR, f'{datetime.now().strftime("%Y%m%d-%H%M%S")}.log'))
    file_handler.setFormatter(formatter)

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)

    return logger


logger = get_logger()
