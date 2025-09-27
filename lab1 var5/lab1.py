import argparse
import re


# --- Константы ---
SURNAME_PATTERN = r"Фамилия:\s*(Иванов[а]{0,1})\s*"

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
        print(f"[!] Ошибка: Файл '{filename}' не найден.")
        return None

def write_to_file(filename: str, data_entries: list[str]):
    """
    Записывает список строк в файл, нумеруя каждую запись.

    Args:
        filename: Имя файла для записи.
        data_entries: Список строк для записи.
    """
    try:
        with open(filename, "w+", encoding="utf-8") as file:
            file.write(f"Всего найдено записей: {len(data_entries)}\n")
            for i, entry in enumerate(data_entries, start=1):
                file.write(f"{i})\n" + entry + "\n")
    except IOError:
        print(f"[!] Ошибка: Не удалось записать данные в файл '{filename}'.")

# --- Функции для парсинга данных ---

def parse_command_line_arguments() -> argparse.Namespace:
    """
    Парсит аргументы командной строки.

    Returns:
        Объект Namespace, содержащий разобранные аргументы.
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
        print("[!] Входное содержимое пустое.")
        return []


    data_blocks = re.split(r"^\d+\)\s*", file_content, maxsplit=1, flags=re.MULTILINE)

    if len(data_blocks) < 2: 
        print("[!] Не удалось найти ожидаемый формат разделения записей.")
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
        return

    parsed_records = parse_records(file_content)

    print(f"Всего найдено записей с фамилией 'Иванов(а)': {len(parsed_records)}")
    for i, record in enumerate(parsed_records, start=1):
        print(f"{i})\n" + record)

    if args.output_file:
        write_to_file(args.output_file, parsed_records)

# --- Запуск скрипта ---

if __name__ == "__main__":
    main()
