import argparse
import re
from datetime import datetime


def parse_console() -> argparse.Namespace:
    """
    Парсер для аргументов в консоли
    """
    parser = argparse.ArgumentParser(description='Фильтрация анкет по корректности дат рождения')
    parser.add_argument("r_file", type=str, help="Путь к исходному файлу с анкетами")
    parser.add_argument("w_file", type=str, help="Путь для сохранения файла с корректными анкетами")
    args = parser.parse_args()
    return args


def is_valid_real_date(date_str: str) -> bool:
    """
    Проверяет, является ли дата реально существующей
    """
    pattern = r'^\s*(0[1-9]|[12][0-9]|3[01])\.(0[1-9]|1[0-2])\.(19[0-9]{2}|20[0-1][0-9]|202[0-5])\s*$'
    if not re.match(pattern, date_str):
        return False
    
    try:
        
        date_str_clean = date_str.strip()
        datetime.strptime(date_str_clean, '%d.%m.%Y')
        return True
    except ValueError:
        return False


def find_incorrect_birthdates(text: str) -> tuple[list, list]:
    """
    Находит анкеты с некорректными датами рождения и разделяет их
    Возвращает: (анкеты_с_некорректными_датами, анкеты_с_корректными_датами)
    """
    profiles = re.split(r'\n(?:\d+\)\s*\n)', text)
    
    incorrect_profiles = []
    correct_profiles = []
    
    for profile in profiles:
        if not profile.strip(): 
            continue
            
        # Ищем дату рождения в анкете
        date_match = re.search(r'Дата[:\s]*рождения[:\s]*([^\n]+)', profile, re.IGNORECASE)
        
        if date_match:
            date_str = date_match.group(1).strip()
            # Проверяем реальность даты
            if is_valid_real_date(date_str):
                correct_profiles.append(profile)
            else:
                incorrect_profiles.append(profile)
        else:
            # Если дата рождения не найдена вообще - считаем некорректной
            incorrect_profiles.append(profile)
    
    return incorrect_profiles, correct_profiles


def read_file(filename: str) -> str:
    with open(filename, 'r', encoding='utf-8') as file:
        return file.read()


def write_file(filename: str, profiles: list) -> None:
    with open(filename, 'w', encoding='utf-8') as file:
        for i, profile in enumerate(profiles, 1):
            file.write(f"{i})\n{profile}\n\n")


def display_incorrect_profiles(profiles: list) -> None:
    """
    Выводит анкеты с некорректными датами рождения на экран
    """
    if not profiles:
        print("Анкет с некорректными датами рождения не найдено.")
        return
    
    print(f"\n{'='*60}")
    print(f"НАЙДЕНО АНКЕТ С НЕКОРРЕКТНЫМИ ДАТАМИ РОЖДЕНИЯ: {len(profiles)}")
    print(f"{'='*60}")
    
    for i, profile in enumerate(profiles, 1):
        print(f"\n--- Анкета {i} ---")
        print(profile)
        print("-" * 40)


def main() -> None:
    try:
        args = parse_console()
        text = read_file(args.r_file)
        
        # Находим анкеты с некорректными датами рождения
        incorrect_profiles, correct_profiles = find_incorrect_birthdates(text)
        
        # Выводим некорректные анкеты на экран
        display_incorrect_profiles(incorrect_profiles)
        
        # Сохраняем корректные анкеты в новый файл
        write_file(args.w_file, correct_profiles)
        
        # Выводим статистику
        print(f"\n{'='*60}")
        print("РЕЗУЛЬТАТЫ ОБРАБОТКИ:")
        print(f"{'='*60}")
        print(f"Всего обработано анкет: {len(incorrect_profiles) + len(correct_profiles)}")
        print(f"Найдено с некорректными датами: {len(incorrect_profiles)}")
        print(f"Оставлено корректных анкет: {len(correct_profiles)}")
        print(f"Корректные анкеты сохранены в файл: {args.w_file}")
        
    except FileNotFoundError:
        print("Ошибка: Исходный файл не найден")
    except Exception as e:
        print(f"Ошибка при обработке файла: {e}")


if __name__ == "__main__":
    main()
