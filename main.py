import argparse
import re


def parse_command_line_arguments() -> str:
    """
    Разбирает аргументы командной строки
    Returns: имя файла с анкетами
    """
    parser = argparse.ArgumentParser(exit_on_error=False)
    parser.add_argument("input_file", type=str, help = "File_name")
    args = parser.parse_args()
    return args.input_file


def read_file(filename: str) -> list:
    """
    Построчное чтение файла
    :param filename: имя файла
    :return: список строк файла
    """

    with open(filename, "r") as file:
        lines = file.readlines()
        return lines

def create_list_of_profiles(lines_from_file: list[str]) -> list[list[str]]:
    """
    Формирование списка анкет
    :param lines_from_file: Список строк, прочитанных из файла с анкетами
    :return: Список анкет
    """
    list_of_profiles = []
    profile = []
    for num_str in lines_from_file:
        if num_str != "\n":
            profile.append(num_str)
        if len(profile) == 7:
            list_of_profiles.append(profile.copy())
            profile.clear()
    return list_of_profiles

def main() -> None:
    # Получение имени файла с анкетами из командной строки
    file_name = parse_command_line_arguments()

    # Чтение файла по строчно
    lines = read_file(file_name)
    
    # Формирование списка анкет
    list_of_profiles = create_list_of_profiles(lines)
    print(list_of_profiles)

if __name__ == "__main__":
    main()
