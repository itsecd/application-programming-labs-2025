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


def main():
    """
    Главная функция
    """

    try:
        args = parse_arguments()
        lines = read_file(args.filename)
        print(f"Файл {args.filename} успешно прочитан")
    except Exception as e:
        print(f"Ошибка: {e}")


if __name__ == '__main__':
    main()