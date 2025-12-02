import argparse
import re
import sys
from datetime import datetime
from typing import List, Dict, Tuple, Optional


def read_file(filename: str) -> List[str]:
    """Чтение файла и возвращение списка строк"""
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            return file.readlines()
    except FileNotFoundError:
        raise FileNotFoundError(f"Файл {filename} не найден")
    except Exception as e:
        raise Exception(f"Ошибка при чтении файла: {e}")


def parse_profiles(lines: List[str]) -> List[Dict[str, str]]:
    """Парсинг анкет из списка строк"""
    profiles = []
    current_profile = {}

    for line in lines:
        line = line.strip()

        if not line:
            continue

        if re.match(r'^\d+\)$', line):
            if current_profile:  
                profiles.append(current_profile)
            current_profile = {}
            continue

        if 'surname' not in current_profile:
            surname = re.sub(r'^Фамилия:\s*', '', line)
            current_profile['surname'] = surname
        elif 'name' not in current_profile:
            name = re.sub(r'^Имя:\s*', '', line)
            current_profile['name'] = name
        elif 'gender' not in current_profile:
            gender = re.sub(r'^Пол:\s*', '', line)
            current_profile['gender'] = gender
        elif 'birth_date' not in current_profile:
            birth_date = re.sub(r'^Дата рождения:\s*', '', line)
            current_profile['birth_date'] = birth_date
        elif 'contact' not in current_profile:
            contact = re.sub(r'^Номер телефона или email:\s*', '', line)
            current_profile['contact'] = contact
        elif 'city' not in current_profile:
            city = re.sub(r'^Город:\s*', '', line)
            current_profile['city'] = city

    if current_profile:
        profiles.append(current_profile)

    return profiles


def validate_name(name: str) -> bool:
    """Проверка валидности имени/фамилии - начинаются с заглавной буквы"""
    pattern = r'^[A-ZА-ЯЁ][a-zа-яё\-]*$'
    return bool(re.match(pattern, name))


def sort_profiles_by_names(profiles: List[Dict[str, str]]) -> Tuple[List[Dict[str, str]], List[Dict[str, str]]]:
    """Сортировка анкет по фамилиям и именам в алфавитном порядке"""
    valid_profiles = []
    invalid_profiles = []

    for profile in profiles:
        if (validate_name(profile['surname']) and 
            validate_name(profile['name'])):
            valid_profiles.append(profile)
        else:
            invalid_profiles.append(profile)

    sorted_profiles = sorted(valid_profiles, 
                           key=lambda x: (x['surname'].lower(), x['name'].lower()))

    return sorted_profiles, invalid_profiles


def save_to_file(profiles: List[Dict[str, str]], output_filename: str) -> str:
    """Сохранение результата в указанный файл с сохранением структуры"""
    try:
        with open(output_filename, 'w', encoding='utf-8') as file:
            for i, profile in enumerate(profiles, 1):
                file.write(f"{i})\n")
                file.write(f"Фамилия: {profile['surname']}\n")
                file.write(f"Имя: {profile['name']}\n")
                file.write(f"Пол: {profile['gender']}\n")
                file.write(f"Дата рождения: {profile['birth_date']}\n")
                file.write(f"Номер телефона или email: {profile['contact']}\n")
                file.write(f"Город: {profile['city']}\n\n")

        return output_filename
    except Exception as e:
        raise Exception(f"Ошибка при сохранении файла: {e}")


def filter_and_print_invalid_profiles(invalid_profiles: List[Dict[str, str]]) -> None:
    """Фильтрация и печать невалидных профилей"""
    print("\nНевалидные профили:")
    for profile in invalid_profiles:
        issues = []
        if not validate_name(profile['surname']):
            issues.append("фамилия")
        if not validate_name(profile['name']):
            issues.append("имя")

        print(f"  {profile['surname']} {profile['name']} - невалидные: {', '.join(issues)}")


def print_sorted_profiles(sorted_profiles: List[Dict[str, str]]) -> None:
    """Печать отсортированных профилей"""
    print("\nПервые 20 отсортированных анкет (Фамилия Имя):")
    for i, profile in enumerate(sorted_profiles[:20], 1):
        print(f"{i:2}. {profile['surname']} {profile['name']}")

    if len(sorted_profiles) > 20:
        print(f"... и еще {len(sorted_profiles) - 20} анкет")


def main() -> None:
    parser = argparse.ArgumentParser(description='Сортировка анкет по фамилиям и именам')
    parser.add_argument('input_file', type=str, help='Название входного файла с анкетами')
    parser.add_argument('output_file', type=str, help='Название выходного файла для результата')

    args = parser.parse_args()
    input_filename = args.input_file
    output_filename = args.output_file

    print("Чтение файла...")
    try:
        lines = read_file(input_filename)
    except (FileNotFoundError, Exception) as e:
        print(e)
        sys.exit(1)

    print("Парсинг анкет...")
    profiles = parse_profiles(lines)

    print(f"Найдено анкет: {len(profiles)}")

    print("Сортировка анкет...")
    sorted_profiles, invalid_profiles = sort_profiles_by_names(profiles)

    print(f"Валидных анкет для сортировки: {len(sorted_profiles)}")
    print(f"Невалидных анкет: {len(invalid_profiles)}")

    print_sorted_profiles(sorted_profiles)

    if invalid_profiles:
        filter_and_print_invalid_profiles(invalid_profiles)

    print(f"\nСохранение результата в {output_filename}...")
    try:
        saved_file = save_to_file(sorted_profiles, output_filename)
        print(f"Результат успешно сохранен в файл: {saved_file}")
        print(f"Всего сохранено {len(sorted_profiles)} анкет")
    except Exception as e:
        print(e)
        sys.exit(1)


if __name__ == "__main__":
    main()