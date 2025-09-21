import re


def differentiate_by_anketes(data: str) -> list[str]:
    """
    Дифференцирование данных на анкеты
    """
    return re.split(r"\d{1,}\)", data)


def find_goal_anketes(anketes: list[str]) -> list[str]:
    """
    Поиск женских анкет с именами на букву А
    """
    result = list()
    for ank in anketes:
        if (re.search(r"Имя:\sА\w*\n"
                      r"Пол:\s(?:Ж|ж|женский|Женский)", ank) is not None):
            ank = re.sub(r"^\n", "", ank)
            result += [ank]
    return result


