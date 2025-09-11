import re
import argparse


def find_full_names(filename: str) -> list:
    """
    Функция читает файл, ищет имена и фамилии в списке, приводит их к формату Фамилия И. и возвращает отсортированный по алфавиту список
    """
    try:
        with open(filename, "r", encoding="utf-8") as file:
            data = file.read()
            names = re.findall(r'Имя:\s+\w+', data)
            surnames = re.findall(r'Фамилия:\s+\w+', data)
            res_names = []
            for i in range(len(names)):
                res_names.append(surnames[i][9].upper()+surnames[i][10:] + " " + names[i][5].upper() + ".")
            return sorted(res_names)
    except:
        print("Файл с таким именем не найден, увынск(")
        return []


def write_full_names(filename: str, lst: list) -> None:
    """
    Функция записывает список в указанный файл
    """
    with open(filename, "w", encoding="utf-8") as file:
        if lst:
            if len(lst)>1:
                for i in range(len(lst)-1):
                    file.write(lst[i]+"\n")
            file.write(lst[len(lst)-1])


def main() -> None:
    """
    Главная функция, которая управляет работой программы
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('input_filename', type=str, help='Path to input file')
    parser.add_argument('output_filename', type=str, help='Path to output file')
    args = parser.parse_args()

    lst_full_names = find_full_names(args.input_filename)
    write_full_names(args.output_filename, lst_full_names)


if __name__=='__main__':
    main()
