import string
from random import random


class UtilClass:
    # 生成随机字符串
    @staticmethod
    def generate_random_string(length=10):
        characters = string.ascii_letters + string.digits
        # 使用 random.choices 从字符集中随机选择字符，并连接成字符串
        random_string = ''.join(random.choices(characters, k=length))
        return random_string