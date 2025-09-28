import argparse
import re


# --- Константы ---
SURNAME_PATTERN = r"Фамилия:\s*([Ии]ванов[а]{0,1})\s*"

# --- Функции для работы с файлами ---

def read_file(filename: str) -> str | None:
    """
    Читает содержимое файла.

    Args:
        filename: Имя файла для чтения.

    Returns:
        Содержимое файла в виде строки, или None, если файл не найден.
    """
    try:
        with open(filename, "r", encoding="utf-8") as file:
            return file.read()
    except FileNotFoundError:
        return None

def write_to_file(filename: str, data_entries: list[str]) -> bool:
    """
    Записывает список строк в файл, нумеруя каждую запись.

    Args:
        filename: Имя файла для записи.
        data_entries: Список строк для записи.
    Returns:
        True, если запись прошла успешно, False в случае ошибки.    
    """
    try:
        with open(filename, "w+", encoding="utf-8") as file:
            file.write(f"Всего найдено записей: {len(data_entries)}\n")
            for i, entry in enumerate(data_entries, start=1):
                file.write(f"{i})\n" + entry + "\n")
            return True
    except IOError:
        return False

# --- Функции для парсинга данных ---

def parse_command_line_arguments() -> argparse.Namespace:
    """
    Эта функция настраивает парсер для обработки следующих аргументов:
    - Обязательный входной файл: Указывает путь к файлу, из которого будут считываться данные для парсинга.
    - Опциональный выходной файл: Указывает путь к файлу, куда будут сохранены отфильтрованные данные. Если этот аргумент не указан, результаты выводятся в консоль.

    Returns:
        Объект Namespace, содержащий разобранные аргументы.
        Значение, переданное через
        --input-file, будет доступно как `args.input_file`, а значение для --output-file — как `args.output_file`. Если опциональный аргумент --output-file не был предоставлен пользователем, его соответствующий атрибут (`args.output_file`) будет иметь значение `None`.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-f", "--input-file",
        type=str,
        required=True,     
    )
    parser.add_argument(
        "-o", "--output-file",
        type=str,    
    )
    return parser.parse_args()


def parse_records(file_content: str) -> list[str]:
    """
    Разделяет содержимое файла на записи и фильтрует их по фамилии.
    Ищет записи, содержащие фамилию "Иванов" или "Иванова".

    Args:
        file_content: Строка, содержащая все содержимое файла.

    Returns:
        Список строк, каждая из которых является отфильтрованной записью.
        Возвращает пустой список, если входное содержимое пустое или не удалось распарсить.
    """
    if not file_content:
        return []


    data_blocks = re.split(r"^\d+\)\s*", file_content, maxsplit=1, flags=re.MULTILINE)

    if len(data_blocks) < 2: 
        return []

    
    records_to_process = [
        record.strip() for record in re.split(r"\n\d+\)\s*", data_blocks[1])
        if record.strip()
    ]

    filtered_records = []
    for record in records_to_process:
        
        match = re.search(SURNAME_PATTERN, record)
        if match:
           
            filtered_records.append(record)

    return filtered_records

# --- Основная функция выполнения ---

def main() -> None:
    """
    Основная точка входа в программу.
    Парсит аргументы, читает файл, обрабатывает данные и выводит/записывает результат.
    """
    args = parse_command_line_arguments()

    file_content = read_file(args.input_file)

    if file_content is None:
        print(f"Ошибка: Не удалось прочитать файл '{args.input_file}'.")
        return
    if not file_content.strip():
        print("Входной файл пуст или содержит только пробельные символы.")
        parsed_records = []
    else:
        parsed_records = parse_records(file_content)
    

    print(f"Всего найдено записей с фамилией 'Иванов(а)': {len(parsed_records)}")
    for i, record in enumerate(parsed_records, start=1):
        print(f"{i})\n" + record)

    if args.output_file:
        write_to_file(args.output_file, parsed_records)

# --- Запуск скрипта ---

if __name__ == "__main__":
    main()
