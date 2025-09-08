import re
import argparse
from typing import List, Tuple

KEY_PATTERN = re.compile(
    r"Фамилия:\s*(?P<firstname>.+?)\nИмя:\s*(?P<lastname>.+?)\n"
)
OLD_NUMBER_PATTERN = re.compile(r"^\d+\)")

def parser_t():
    """
    функция нужна для ввода названий файлов
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('first_file', type=str, help='Путь к исходному файлу')
    parser.add_argument('-lf', '--last_file', default='output.txt', type=str, help='Путь к файлу для сохранения результата')

    args = parser.parse_args()
    return args


def read_and_split_into_blocks(filepath: str) -> List[str]:
    """
    читает файл и разделяет его на текстовые блоки по записям.
    """
    try:
        with open(filepath, "r") as file:
            full_text = file.read()
    except FileNotFoundError:
        print(f"Ошибка: Файл '{filepath}' не найден.")
        return []

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
    with open(filepath, "w") as output_file:
        for index, s_tuple in enumerate(sorted_list, 1):
            new_number_str = f"{index})"
            new_block = OLD_NUMBER_PATTERN.sub(new_number_str, s_tuple[2])
            output_file.write(new_block + "\n\n")


def main() -> None:
    """
    главная функция, управляющая всем процессом.
    """

    a = parser_t()

    input_filename = a.first_file
    output_filename = a.last_file

    print(f"Чтение файла '{input_filename}'...")
    all_blocks = read_and_split_into_blocks(input_filename)
    if not all_blocks:
        print("Файл пуст или не найден. Завершение работы.")
        return

    sortable_data = create_sortable_list(all_blocks)
    final_sorted_list = sorted(sortable_data, key=lambda item: (item[0], item[1]))
    write_sorted_blocks_to_file(output_filename, final_sorted_list)

    print("\nПроцесс успешно завершен!")

if __name__ == '__main__':
    main()
