import re
import argparse
from typing import List, Dict, Tuple


def read_file(filename: str) -> List[str]:
    """
    Читает файл и возвращает список строк.
    
    Args:
        filename (str): Имя файла для чтения
        
    Returns:
        List[str]: Список строк файла
    """
    try:
        with open(filename, "r", encoding="utf-8") as file:
            return file.readlines()
    except FileNotFoundError as exc:
        raise FileNotFoundError(f"Файл {filename} не найден") from exc


def main() -> None:
    """
    Основная функция программы.
    """
    # Создание парсера аргументов командной строки
    parser = argparse.ArgumentParser(description='Анализ доменов email в файле данных')
    parser.add_argument('filename', type=str, help='Имя входного файла с данными')
    
    # Парсинг аргументов
    args = parser.parse_args()
    
    print(f"Анализируем файл: {args.filename}")
    
    # Чтение файла
    lines = read_file(args.filename)
    print(f"Прочитано строк: {len(lines)}")


if __name__ == "__main__":
    main()
