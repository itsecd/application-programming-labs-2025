"""
Var_12 Определите, какой код оператора чаще всего 
встречается в телефонных номерах. Выведите
на экран код и количество его повторений.
"""

import argparse
import re
from typing import List, Dict, Tuple, Optional
def open_file(file_path: str) -> Optional[List[str]]:
    """
    Открывает файл и возвращает список строк.
    
    Args:
        file_path (str): Путь к файлу
        
    Returns:
        Optional[List[str]]: Список строк из файла или None в случае ошибки
    """
    try:
        with open(file_path, "r", encoding='utf-8') as file:
            return file.readlines()
    except FileNotFoundError:
        print(f"Error: file '{file_path}' not found.")
        return None
    except IOError as e:
        print(f"Error reading file '{file_path}': {e}")
        return None
def main() -> None:
 
    parser = argparse.ArgumentParser()
    parser.add_argument('name', type=str, help='your name')
    args = parser.parse_args()

    lines = open_file(args.name)
 
    if (lines == None):
        return
    
    pattern = r"(?:\+7|8)[\s\(]*(\d{3})[\s\)]*\d{3}[\s\-]*\d{2}[\s\-]*\d{2}\b"
    
    operator_codes = extract_operator_codes(lines, pattern)
    
    if not operator_codes:
        print("No phone numbers found")
        return
    
    code_counts = count_codes(operator_codes)
    try:
        code, count = max_code(code_counts)
        print(f"Наиболее часто встречающийся код оператора — {code}, встречается {count} раз(а)")
    except ValueError as e:
        print(e)


if __name__ == "__main__":
    main()