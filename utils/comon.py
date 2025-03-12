import random
import string
import re

def generateToken(uId: int, uname: str) -> str:
    filtered_name = re.sub(r'[^a-zA-Z]', '', uname)
    short_name = (filtered_name[:4] + "xxxx")[:4].lower()
    random_char = random.choice(string.ascii_lowercase + string.digits)
    return f"{uId}{short_name}{random_char}"

