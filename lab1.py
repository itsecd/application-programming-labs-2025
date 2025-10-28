"""Анализ анкет из файла"""

import argparse
import re


def read_file(filename):
    """
    Читает файл и возвращает список строк
    """

    try:
        with open(filename, 'r', encoding='utf-8') as file:
            lines = file.readlines()
        return [line.strip() for line in lines]
    except FileNotFoundError:
        raise FileNotFoundError(f"Файл {filename} не найден")
    except Exception as e:
        raise Exception(f"Ошибка при чтении файла: {e}")


def parse_arguments():
    """
    Парсит аргументы командной строки
    """

    parser = argparse.ArgumentParser(description='Анализ анкет по полу')
    parser.add_argument('filename', help='Имя файла с анкетами')
    return parser.parse_args()


def extract_gender_entries(lines, target_gender='Мужской'):
    """
    Находит анкеты по полу и считает их
    """

    male_entries = []
    current_entry = []
    is_male = False
    entry_count = 0

    for line in lines:
        if not line:
            if current_entry and is_male:
                male_entries.append('\n'.join(current_entry))
                entry_count += 1
            current_entry = []
            is_male = False
        else:
            current_entry.append(line)
            if re.search(r'^Пол:\s*' + re.escape(target_gender), line):
                is_male = True

    if current_entry and is_male:
        male_entries.append('\n'.join(current_entry))
        entry_count += 1

    return entry_count, male_entries


def main():
    """
    Главная функция
    """

    try:
        args = parse_arguments()
        lines = read_file(args.filename)
        count, entries = extract_gender_entries(lines, 'Мужской')
        print(f"Найдено мужских анкет: {count}")
    except Exception as e:
        print(f"Ошибка: {e}")


if __name__ == '__main__':
    main()