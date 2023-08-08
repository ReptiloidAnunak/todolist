import string
import secrets
from bot.models import TgUser


def generate_verification_code():
    symbols = string.ascii_letters + string.digits
    code = "".join(secrets.choice(symbols) for s in range(20))
    return code

print(generate_verification_code)

