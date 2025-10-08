import re
import sys
import argparse

def read_file(filename: str) -> str | None:
    try:
        with open(filename, "r", encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        print(f"Ошибка: Файл '{filename}' не найден.")
        return None
    except Exception as e:
        print(f"Ошибка при чтении файла: {e}")
        return None

def correct_date(day: int, month: int, year: int) -> bool:
    if not (2001 <= year <= 2025):
        return False
    if not (1 <= month <= 12):
        return False 

def main():
    parser = argparse.ArgumentParser(
        description="Извлечение анкет людей, родившихся в 21 веке, из файла data.txt и сохранение их в новый файл."
    )
    parser.add_argument(
        'filename', 
        type=str,
        help='Имя исходного файла для обработки.'
    )
    parser.add_argument(
        '-o', '--output', 
        type=str, 
        default='born_in_21st_century.txt', 
        help='Имя выходного файла для сохранения результатов.'
    )
    parser.add_argument(
        '-v', '--verbose', 
        action='store_true', 
        help='Вывод на экран анкеты людей, родившихся в 21 веке.'
    )
    
    args = parser.parse_args()

if __name__ == "__main__":
    main()