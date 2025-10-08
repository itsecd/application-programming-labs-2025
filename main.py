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

    days_in_month = [31, 29 if is_leap_year(year) else 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    return 1 <= day <= days_in_month[month - 1] if 1 <= month <= 12 else False

def split_file(text: str) -> list[str]:
    return re.split(r'\n\s*\n+', text.strip())

def is_leap_year(year: int) -> bool:
    return (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)

def extract_born_in_21st_century(forms: list[str]) -> list[str]:
    pattern = r'\b(\d{1,2}).(\d{1,2}).(20\d{2})\b'
    result = []
    for form in forms:
        match = re.search(pattern, form)
        if match:
            day, month, year = map(int, match.groups())
            if correct_date(day, month, year):
                result.append(form)
    return result

def save_to_file(data: list[str], output_filename: str):
    try:
        with open(output_filename, "w", encoding='utf-8') as f:
            for item in data:
                f.write(item + "\n\n")
        print(f"Результаты сохранены в файл: '{output_filename}'")
    except Exception as e:
        print(f"Ошибка при сохранении в файл '{output_filename}': {e}")

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
        help='Имя выходного файла для сохранения результатов (по умолчанию: born_in_21st_century.txt).'
    )
    parser.add_argument(
        '-v', '--verbose', 
        action='store_true', 
        help='Вывод на экран анкеты людей, родившихся в 21 веке.'
    )
    
    args = parser.parse_args()

    content = read_file(args.filename)
    
    if content is not None:
        forms = split_file(content)
        born_in_21st_century = extract_born_in_21st_century(forms)
        
        print(f"Люди, родившиеся в 21 веке: {len(born_in_21st_century)}.")
        
        if born_in_21st_century: 
            save_to_file(born_in_21st_century, args.output)
        else:
            print("Анкеты не найдены с датами рождения 21 века для сохранения.")

        if args.verbose:
            print("\nАнкеты людей, которые родились в 21 веке:")
            if born_in_21st_century:
                for form in born_in_21st_century:
                    print(form)
            else:
                print("Не найдены.")
    else:
        print("\nЧтение файла не удалось.")

if __name__ == "__main__":
    main()