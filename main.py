#!/usr/bin/env python3
"""
Лабораторная работа 1 - Обработка анкетных данных
"""

import argparse
import re
from datetime import datetime
from typing import List


def parse_arguments() -> argparse.Namespace:
    """
    Парсинг аргументов командной строки
    """
    parser = argparse.ArgumentParser(description='Обработка анкетных данных')
    parser.add_argument("input_file", type=str, help="Имя входного файла")
    parser.add_argument("-o", "--output", type=str, default="result.txt", help="Имя выходного файла")
    return parser.parse_args()


def read_file(filename: str) -> str:
    """
    Чтение содержимого файла
    """
    try:
        with open(filename, 'r', encoding="utf-8") as file:
            return file.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"Файл {filename} не найден")


def extract_profiles(data: str) -> List[List[str]]:
    """
    Извлечение профилей из данных
    """
    profiles = []
    #разделяю по шаблону на "1)", "2)", "3)" и т.д.
    blocks = re.split(r'\n\s*\d+\)\s*\n', data)
    
    for block in blocks:
        if block.strip():
            profile = extract_profile_data(block)
            if profile:
                profiles.append(profile)
    
    return profiles


def extract_profile_data(block: str) -> List[str]:
    """
    Извлечение данных одного профиля из блока
    """
    lines = [line.strip() for line in block.split('\n') if line.strip()]
    
    surname = "-"
    name = "-"
    gender = "-"
    birth_date = "-"
    contact = "-"
    city = "-"
    
    for line in lines:
        if line.startswith('Фамилия:'):
            surname = line.replace('Фамилия:', '').strip()
        elif line.startswith('Имя:'):
            name = line.replace('Имя:', '').strip()
        elif line.startswith('Пол:'):
            gender = line.replace('Пол:', '').strip()
        elif line.startswith('Дата рождения:'):
            birth_date = line.replace('Дата рождения:', '').strip()
        elif line.startswith('Номер телефона или email:'):
            contact = line.replace('Номер телефона или email:', '').strip()
        elif line.startswith('Город:'):
            city = line.replace('Город:', '').strip()
    
    return [surname, name, gender, birth_date, contact, city]


def process_contact(contact: str) -> str:
    """
    Обработка и стандартизация контакта
    """
    if not contact or contact == '-':
        return '-'
    
    if is_valid_phone(contact):
        return normalize_phone(contact)
    elif is_valid_email(contact):
        return contact
    
    return '-'


def is_valid_phone(phone: str) -> bool:
    """
    Проверка валидности номера телефона
    """
    if not phone:
        return False
    
    digits = re.sub(r'\D', '', phone)
    return len(digits) == 11 and digits.startswith(('7', '8'))


def is_valid_email(email: str) -> bool:
    """
    Проверка валидности email
    """
    if not email or '@' not in email:
        return False
    
    if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
        return False
    
    domain = email.split('@')[1].lower()
    return domain in ['gmail.com', 'mail.ru', 'yandex.ru']


def normalize_phone(phone: str) -> str:
    """
    Приведение телефона к формату 8 (012) 345-67-89
    """
    digits = re.sub(r'\D', '', phone)
    
    if digits.startswith('7'):
        digits = '8' + digits[1:]
    elif digits.startswith('+7'):
        digits = '8' + digits[2:]
    
    if len(digits) == 11:
        return f"8 ({digits[1:4]}) {digits[4:7]}-{digits[7:9]}-{digits[9:]}"
    
    return '-'


def process_city(city: str) -> str:
    """
    Проверка и обработка города
    """
    if not city or city == '-':
        return '-'
    
    #убираю г.
    city_clean = re.sub(r'^г\.?\s*', '', city.strip(), flags=re.IGNORECASE)
    city_clean = city_clean.strip()
    
    if not city_clean:
        return '-'
    
    return city_clean


def process_name(name: str) -> str:
    """
    Проверка и обработка имени/фамилии
    """
    if not name or name == '-':
        return '-'
    
    if name and name[0].islower():
        #если первая буква маленькая, делаем ее заглавной
        return name[0].upper() + name[1:]
    elif name and name[0].isupper():
        return name
    
    return '-'


def process_gender(gender: str) -> str:
    """
    Стандартизация пола
    """
    if not gender or gender == '-':
        return '-'
    
    gender_lower = gender.lower()
    
    if any(word in gender_lower for word in ['муж', 'м', 'male', 'm']):
        return 'Мужской'
    elif any(word in gender_lower for word in ['жен', 'ж', 'female', 'f']):
        return 'Женский'
    
    return '-'


def process_birth_date(date: str) -> str:
    """
    Обработка и стандартизация даты рождения
    """
    if not date or date == '-':
        return '-'
    
    if not is_valid_date(date):
        return '-'
    
    return normalize_date(date)


def is_valid_date(date_str: str) -> bool:
    """
    Проверка валидности даты
    """
    if not date_str:
        return False
    
    #проверка формата даты
    date_pattern = r'^(\d{1,2})[/.-](\d{1,2})[/.-](\d{4})$'
    match = re.match(date_pattern, date_str)
    
    if not match:
        return False
    
    day, month, year = match.groups()
    
    try:
        day_int, month_int, year_int = int(day), int(month), int(year)
        
        current_year = datetime.now().year
        if year_int < 1900 or year_int > current_year:
            return False
    
        if month_int < 1 or month_int > 12:
            return False
        
        if day_int < 1 or day_int > 31:
            return False
        
        if month_int in [4, 6, 9, 11] and day_int > 30:
            return False

        if month_int == 2:
            if (year_int % 4 == 0 and year_int % 100 != 0) or (year_int % 400 == 0):
                if day_int > 29:
                    return False
            else:
                if day_int > 28:
                    return False
        
        return True
        
    except ValueError:
        return False


def normalize_date(date_str: str) -> str:
    """
    Приведение даты к формату ДД.ММ.ГГГГ
    """
    if not date_str:
        return '-'
    
    # Парсим дату
    date_pattern = r'^(\d{1,2})[/.-](\d{1,2})[/.-](\d{4})$'
    match = re.match(date_pattern, date_str)
    
    if not match:
        return '-'
    
    day, month, year = match.groups()
    
    try:
        day_int, month_int, year_int = int(day), int(month), int(year)
        return f"{day_int:02d}.{month_int:02d}.{year_int}"
    except ValueError:
        return '-'


def process_profiles(profiles: List[List[str]]) -> List[List[str]]:
    """
    Обработка всех профилей
    """
    processed_profiles = []
    
    for profile in profiles:
        surname, name, gender, birth_date, contact, city = profile
        
        processed_profile = [
            process_name(surname),
            process_name(name),
            process_gender(gender),
            process_birth_date(birth_date),
            process_contact(contact),
            process_city(city)
        ]
        processed_profiles.append(processed_profile)
    
    return processed_profiles


def write_profiles_to_file(filename: str, profiles: List[List[str]]) -> None:
    """
    Запись профилей в файл
    """
    with open(filename, 'w', encoding="utf-8") as file:
        for i, profile in enumerate(profiles, 1):
            file.write(f"{i})\n")
            file.write(f"Фамилия: {profile[0]}\n")
            file.write(f"Имя: {profile[1]}\n")
            file.write(f"Пол: {profile[2]}\n")
            file.write(f"Дата рождения: {profile[3]}\n")
            file.write(f"Номер телефона или email: {profile[4]}\n")
            file.write(f"Город: {profile[5]}\n\n")


def main() -> None:
    """
    Основная функция программы
    """
    try:
        args = parse_arguments()
        
        #чтение файла
        data = read_file(args.input_file)
        print(f"Файл {args.input_file} прочитан успешно")
        
        #извлечение профилей
        profiles = extract_profiles(data)
        print(f"Найдено профилей: {len(profiles)}")
        
        #обработка профилей
        processed_profiles = process_profiles(profiles)
        
        #запись результата
        write_profiles_to_file(args.output, processed_profiles)
        print(f"Результат сохранен в {args.output}")
        
            
    except FileNotFoundError as e:
        print(f"Ошибка: {e}")
    except Exception as e:
        print(f"Ошибка при выполнении программы: {e}")


if __name__ == "__main__":
    main()
