import re

def read_file() -> str:
    """
    Операция чтения данных из файла в строку
    """
    try:
        with open("data.txt", encoding="utf-8") as file:
            text = file.read()
        return text
    except ValueError as exc:
        print(f"Data Error: {exc}")


def differentiate_by_anketes(data:str)->list[str]:
    """
    Дифференцирование данных на анкеты
    """
    return re.split(r"\d{1,}\)", data)


def find_goal_anketes(anketes:list[str])->list[str]:
    """
    Поиск женских анкет с именами на букву А
    """
    result=list()
    for ank in anketes:
        if re.fullmatch(r"Имя:\s\b(А\w*) Пол:\s([Жж])",ank):
            result+=[ank]
            print(ank)
            input()
    return ank

data = read_file()
data_list = differentiate_by_anketes(data)

res = find_goal_anketes(data_list)
print(res)
