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
    parser.add_argument('-o', '--output', default='male_entries.txt',
                       help='Имя файла для сохранения результатов (по умолчанию: male_entries.txt)')
    return parser.parse_args()


def extract_gender_entries(lines, target_gender='Мужской'):
    """
    Находит анкеты по полу и считает их,также сделаны
    валидные форматы для мужского пола: М, м, Мужской, мужской.
    """

    male_entries = []
    current_entry = []
    is_male = False
    entry_count = 0

    male_pattern = re.compile(r'^Пол:\s*(Мужской|мужской|М|м)\b')

    for line in lines:
        if not line:
            if current_entry and is_male:
                male_entries.append('\n'.join(current_entry))
                entry_count += 1
            current_entry = []
            is_male = False
        else:
            current_entry.append(line)
            if male_pattern.search(line):
                is_male = True

    if current_entry and is_male:
        male_entries.append('\n'.join(current_entry))
        entry_count += 1

    return entry_count, male_entries

def save_results(entries, output_filename):
    """
    Сохраняет анкеты в файл
    """

    try:
        with open(output_filename, 'w', encoding='utf-8') as file:
            for i, entry in enumerate(entries, 1):
                file.write(f"Анкета #{i}:\n")
                file.write(entry)
                file.write("\n\n" + "="*50 + "\n\n")
        print(f"Анкеты сохранены в файл: {output_filename}")
    except Exception as e:
        raise Exception(f"Ошибка при сохранении файла: {e}")


def count_male_entries(entries):
    """
    Считает количество анкет мужчин в списке
    """

    return len(entries)


def main():
    """
    Главная функция
    """

    try:
        args = parse_arguments()
        lines = read_file(args.filename)
        count, entries = extract_gender_entries(lines, 'Мужской')
        male_count = count_male_entries(entries)
        print(f"Количество мужских анкет: {male_count}")
        if male_count > 0:
            save_results(entries, args.output)
        else:
            print("Мужские анкеты не найдены, файл не создан.")

    except Exception as e:
        print(f"Ошибка: {e}")

if __name__ == '__main__':
    main()
