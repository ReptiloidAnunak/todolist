import string
import secrets
from bot.models import TgUser


def generate_verification_code():
    symbols = string.ascii_letters + string.digits
    code = "".join(secrets.choice(symbols) for s in range(20))
    return code


def create_goal_list_message(g_list: list):
    title = "\n\nВАШ СПИСОК ЦЕЛЕЙ\n\n"
    points = []
    for goal in g_list:
        number = g_list.index(goal) + 1
        point = f"\n{str(number)}. {goal}"
        points.append(point)

    "\n".join(points)
    points = "\n".join(points)
    result = title + points
    return result


