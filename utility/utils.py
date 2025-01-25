import os
import random
import string
from utility.constant import Constant
import logging


class Utils:
    @staticmethod
    def generate_request_id() -> str:
        prefix = "JBRQ"
        N = int(Constant.id_length)
        id = prefix + ''.join(random.choices(string.digits, k= N - len(prefix) - 20)) +''.join(random.choices(string.ascii_uppercase + string.digits, k=20))
        return id
    
    @staticmethod
    def setup_logging(log_file='record.log', level=logging.DEBUG):
        logging.basicConfig(
            filename=log_file,
            level=level,
            format='%(asctime)s | %(levelname)s | %(lineno)d | \n %(message)-20s'
        )
        # Add console logging for easier debugging
        console_handler = logging.StreamHandler()
        console_handler.setLevel(level)
        console_formatter = logging.Formatter(
            '%(asctime)s | %(levelname)s | %(lineno)d | \n %(message)-20s'
        )
        console_handler.setFormatter(console_formatter)
        logging.getLogger().addHandler(console_handler)
