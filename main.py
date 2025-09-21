import re
import argparse


def read_file(filename: str) -> str:
    """
    Операция чтения данных из файла в строку
    """
    try:
        with open(filename, encoding="utf-8") as file:
            text = file.read()
        return text
    except ValueError as exc:
        print(f"Data Error: {exc}")


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


def write_data(data: list[str]) -> None:
    with open("result.txt", "+w", encoding="utf-8") as f:
        for i in range(len(data)):
            f.write(f"{i+1})\n")
            f.write(data[i])


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', type=str, help='name of scanning file')
    args = parser.parse_args()
    data = read_file(args.filename)
    data_list = differentiate_by_anketes(data)
    res = find_goal_anketes(data_list)
    write_data(res)
    print(len(res))


if __name__ == "__main__":
    main()
