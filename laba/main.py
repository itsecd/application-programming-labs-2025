import re
import argparse
from typing import List, Tuple
import sys

KEY_PATTERN = re.compile(
    r"Фамилия:\s*(?P<lastname>.+?)\nИмя:\s*(?P<firstname>.+?)\n"
)
OLD_NUMBER_PATTERN = re.compile(r"^\d+\)")

def parser_t():
    """
    функция нужна для ввода названий файлов
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('source_file', type=str, help='Путь к исходному файлу')
    parser.add_argument('-of', '--output_file', default='output.txt', type=str, help='Путь к файлу для сохранения результата')

    args = parser.parse_args()
    return args

def open_file(filepath):
    """
    функция для прочтения файла
    """
    with open(filepath, "r", encoding="utf-8") as file:
        full_text = file.read()
    return full_text


def split_into_blocks(full_text: str) -> List[str]:
    """
    разделяет текст на текстовые блоки по записям.
    """
    raw_blocks = re.split(r'(\d+\)\n)', full_text)[1:]
    grouped_blocks = [
        raw_blocks[i] + raw_blocks[i+1]
        for i in range(0, len(raw_blocks), 2)
    ]
    return grouped_blocks


def create_sortable_list(blocks: List[str]) -> List[Tuple[str, str, str]]:
    """
    создает список кортежей для сортировки из текстовых блоков.
    """
    list_sortable = []
    for block_text in blocks:
        match = KEY_PATTERN.search(block_text)
        if match:
            firstname = match.group('firstname').strip().lower()
            lastname = match.group('lastname').strip().lower()
            list_sortable.append((firstname, lastname, block_text))
    return list_sortable


def write_sorted_blocks_to_file(
    filepath: str,
    sorted_list: List[Tuple[str, str, str]]
) -> None:
    """
    Записывает отсортированные блоки в файл с новой нумерацией.
    """
    with open(filepath, "w", encoding="utf-8") as output_file:
        for index, s_tuple in enumerate(sorted_list, 1):
            new_number_str = f"{index})"
            new_block = OLD_NUMBER_PATTERN.sub(new_number_str, s_tuple[2])
            output_file.write(new_block + "\n\n")


def main() -> None:
    """
    главная функция, управляющая всем процессом.
    """

    a = parser_t()

    input_filename = a.source_file
    output_filename = a.output_file

    print(f"Чтение файла '{input_filename}'...")
    try:
        full_text = open_file(input_filename)
        blocks = split_into_blocks(full_text)

        sortable_data = create_sortable_list(blocks)
        final_sorted_list = sorted(sortable_data, key=lambda item: (item[1], item[0]))
        write_sorted_blocks_to_file(output_filename, final_sorted_list)

        print("\nПроцесс успешно завершен!")
    except FileNotFoundError:
        print("\nПроцесс завершился с ошибкой")
        sys.exit()

if __name__ == '__main__':
    main()