import string
import secrets

from goals.models import Goal, GoalCategory


def generate_verification_code() -> str:
    """Генерирует код для верификации
    пользователя Телеграм в приложении"""
    symbols = string.ascii_letters + string.digits
    code = "".join(secrets.choice(symbols) for s in range(20))
    return code


def create_goal_list_message(g_list: list) -> str:
    """Создает список целей пользователя
    для отправки телеграм-ботом"""
    title = "\n\nВАШ СПИСОК ЦЕЛЕЙ\n\n"
    points = []
    for goal in g_list:
        number = g_list.index(goal) + 1
        point = f"\n{str(number)}. {goal}"
        points.append(point)

    points = "\n".join(points)
    result = title + points
    return result


def create_categories_list(categories_dict: dict) -> str:
    """Создает список категорий пользователя
    для отправки телеграм-ботом"""
    title = "\n\nВаши категории:\n\n"
    cat_list = []
    for key in categories_dict:
        point = f"[{key}]   {categories_dict[key]}"
        cat_list.append(point)
    points = "\n".join(cat_list)
    result = title + points
    return result


def confirm_goal_creation(new_goal: Goal) -> str:
    """Создает сообщение об успешном создании цели"""
    message = (f"Цель создана!\n{new_goal.title}"
               f"\nКатегория: {new_goal.category}"""
               f"\nВремя создания: {new_goal.created}")
    return message
