import io
import argparse
import re


def read_file(filename: str) -> str:
    """
    Чтение файла для дальнейшей работы с ним
    """
    try:
        file = open(filename, "r")
        print(f"File {filename} is parsed!")
        text = file.read()
        file.close()
        return text
    except FileNotFoundError:
        print(f"Sorry, {filename} dont found!!!")
        return ""


def create_file(output_filename, content="", encoding="utf-8"):
    """
    Создает новый файл для записи

    """
    try:
        with open(output_filename, 'w', encoding=encoding) as file:
            file.write(content)
        print(f"Файл '{output_filename}' успешно создан")
        return True
    except Exception as e:
        print(f"Ошибка при создании файла '{output_filename}': {e}")
        return False


def process_and_sort_names(filename):
    """
    Читает файл с данными, сортирует записи и преобразует к формату 'Фамилия И.'

    """
    result = []

    with open(filename, 'r') as file:
        content = file.read()

    # Разделяем на отдельные записи
    records = content.split('\n\n')

    for record in records:
        if not record.strip():
            continue

        lines = record.strip().split('\n')
        surname = ""
        name = ""

        for line in lines:
            if line.startswith('Фамилия:'):
                surname = line.replace('Фамилия:', '').strip()
            elif line.startswith('Имя:'):
                name = line.replace('Имя:', '').strip()

        # Приводим к правильному регистру
        if surname:
            surname = surname.capitalize()
        if name:
            name = name.capitalize()

        # Форматируем в "Фамилия И."
        if surname and name:
            formatted_name = f"{surname} {name[0]}."
            result.append(formatted_name)

    # Сортируем по фамилии, затем по имени
    result.sort()

    return result


def list_to_string(lst, separator=''):
    """
    Преобразует список в строку, соединяя элементы через разделитель

    """
    return separator.join(str(item) for item in lst)


def split_by_dot_newline(sorted_names):
    """
    Разделяет строку по точке и записывает каждый элемент с новой строки

    """
    if not sorted_names:
        return ""

    # Разделяем по точке и убираем пустые элементы
    parts = [part.strip() for part in sorted_names.split('.') if part.strip()]

    # Соединяем с переносами строк
    return '\n'.join(part + '.' for part in parts)


def get_args() -> str:
    parser = argparse.ArgumentParser(
        prog='Обработка текстовых данных ')  # создание экземпляра парсера
    # добавление позиционного аргумента командной строки
    parser.add_argument('filename', type=str, help='filename')
    parser.add_argument('output_filename', type=str,
                        help='output_filename')  # имя выходного файла
    args = parser.parse_args()  # парсинг аргументов
    if args.filename is None or args.output_filename is None:
        return ""
    return [args.filename, args.output_filename]


def main() -> None:
    filepath, output_filename = get_args()
    text = read_file(filepath)
    out_file = print()
    sorted_names = process_and_sort_names('data.txt')
    sort = list_to_string(sorted_names)

    ofile = create_file(output_filename, split_by_dot_newline(sort))


if __name__ == "__main__":
    main()
