import argparse
import re
import sys

def parse_command_line_arguments() -> tuple[str, str]:
    """
    Разбирает аргументы командной строки
    Returns: имя файла с анкетами
    """
    parser = argparse.ArgumentParser(exit_on_error=False)
    parser.add_argument("input_file", type=str, help = "File_name")
    parser.add_argument("output_file", type=str, help="File_name")
    try:
        args = parser.parse_args()
        return args.input_file, args.output_file
    except argparse.ArgumentError as e:
        raise ValueError(f"Ошибка при разборе аргументов командной строки: {e}")

def read_file(filename: str) -> list:
    """
    Построчное чтение файла
    :param filename: имя файла
    :return: список строк файла
    """
    try:
        with open(filename, "r") as file:
            lines = file.readlines()
            return lines
    except FileNotFoundError:
        raise FileNotFoundError(f"Ошибка: Файл '{filename}' не найден.")
    except IOError as e:
        raise IOError(f"Ошибка при чтении файла '{filename}': {e}")
    except Exception as e:
        raise Exception(f"Непредвиденная ошибка при чтении файла '{filename}': {e}")

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


def filter_profiles(last_name_pattern: re.Pattern, list_of_profiles: list[list[str]]) -> list[list[str]]:
    """
    Формирование списка анкет, удовлетворяющих валидному формату фамилии
    :param last_name_pattern: регулярное выражение для фамилии
    :param list_of_profiles: список анкет
    :return: список анкет, удовлетворяющих валидному формату фамилии
    """
    matching_profiles = []
    for profile in list_of_profiles:
        match_last_name_value = re.match(r'Фамилия:\s*(.+)', profile[1])
        last_name = match_last_name_value.group(1).strip()
        if last_name_pattern.match(last_name):
            matching_profiles.append(profile)
    return matching_profiles

def write_in_file(matching_profiles: list[list[str]], filename: str) -> None:
    """
    Запись найденных анкет в файл
    :param matching_profiles: список анкет, удовлетворяющих валидному формату фамилии
    :param filename: имя файла
    :return: ничего
    """
    try:
        with open(filename, 'w', encoding='utf-8') as file:
            for profile in matching_profiles:
                file.write("".join(profile) + "\n")
    except IOError as e:
        raise IOError(f"Ошибка при записи файла 'New file.txt': {e}")
    except Exception as e:
        raise Exception(f"Непредвиденная ошибка при записи файла 'New file.txt': {e}")

def main() -> None:
    # Получение имени файла с анкетами из командной строки
    try:
        file_names = parse_command_line_arguments()

        # Чтение файла по строчно
        lines = read_file(file_names[0])

        # Формирование списка анкет
        list_of_profiles = create_list_of_profiles(lines)

        # Определение регулярного выражения для фамилии
        last_name_pattern = re.compile(r'^[А-Я][а-я]*(ов|ова)$')

        # Формирование списка анкет, удовлетворяющих валидному формату фамилии
        matching_profiles = filter_profiles(last_name_pattern, list_of_profiles)

        # Вывод количества найденных анкет
        print(f"Найдено: {len(matching_profiles)} человек с фамилиями, оканчивающимися на 'ов' или 'ова'.")

        # Запись найденных анкет в новый файл
        write_in_file(matching_profiles, file_names[1])

    except ValueError as e:
        print(f"Ошибка запуска: {e}")
        sys.exit(1)
    except FileNotFoundError as e:
        print(f"Ошибка файла: {e}")
        sys.exit(1)
    except IOError as e:
        print(f"Ошибка ввода/вывода: {e}")
        sys.exit(1)
    except TypeError as e:
        print(f"Ошибка типа данных во время обработки: {e}")
        sys.exit(1)
    except AttributeError as e:
        print(f"Ошибка обработки данных анкеты (возможно, неверный формат строки): {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Произошла непредвиденная критическая ошибка: {e}")
        sys.exit(1)
if __name__ == "__main__":
    main()