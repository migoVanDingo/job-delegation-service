import os
import random
import string
from utility.constant import Constant


class Utils:
    @staticmethod
    def generate_request_id() -> str:
        prefix = "JBRQ"
        N = int(Constant.id_length)
        id = prefix + ''.join(random.choices(string.digits, k= N - len(prefix) - 20)) +''.join(random.choices(string.ascii_uppercase + string.digits, k=20))
        return id