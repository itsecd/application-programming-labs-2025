import argparse
import re
from typing import List, Tuple
from collections import Counter


def read_file(filename: str) -> List[str]:
    """
    Читает файл и возвращает список строк.
    """
    try:
        with open(filename, "r", encoding="utf-8") as file:
            return file.readlines()
    except FileNotFoundError as exc:
        raise FileNotFoundError(f"Файл {filename} не найден") from exc


def extract_names_from_file(filename: str) -> List[str]:
    """
    Извлекает имена из файла после метки 'Имя:' с использованием регулярного выражения.
    """
    lines = read_file(filename)
    names = []
    
    # Регулярное выражение для извлечения имени после "Имя:"
    # Группа ([^:\n]+) захватывает все символы кроме двоеточия и переноса строки
    name_pattern = r'^Имя:\s*([^:\n]+)$'
    
    for line in lines:
        line = line.strip()
        match = re.match(name_pattern, line)
        if match:
            name = match.group(1).strip()
            if name:
                names.append(name)
    
    return names


def find_most_common_name(names: List[str]) -> Tuple[str, int]:
    """
    Находит самое частое имя и количество его вхождений.
    
    Returns:
        Tuple[str, int]: (самое_частое_имя, количество)
    """
    if not names:
        return ("", 0)
    
    name_counter = Counter(names)
    return name_counter.most_common(1)[0]


def main() -> None:
    """
    Основная функция программы.
    """
    parser = argparse.ArgumentParser(description='Находит самое частое имя в файле')
    parser.add_argument('filename', type=str, help='Имя входного файла с данными')
    
    try:
        args = parser.parse_args()
        
        names = extract_names_from_file(args.filename)
        
        if not names:
            print("Имена не найдены")
            return
        
        most_common_name, count = find_most_common_name(names)
        
        print(f"Самое частое имя: '{most_common_name}' (встречается {count} раз)")
        
    except Exception as exc:
        print(f"Ошибка: {exc}")


if __name__ == "__main__":
    main()

