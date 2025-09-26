#!/usr/bin/env python3
"""
Лабораторная работа 1 - Обработка анкетных данных
"""

import re

def main():
    print("Лабораторная работа 1 - Обработка данных")
    
    # Автоматически используем data.txt
    input_file = "data.txt"
    output_file = "result.txt"
    
    # Читаем файл
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            content = f.read()
        print(f"Файл {input_file} прочитан успешно")
    except FileNotFoundError:
        print(f"Файл {input_file} не найден! Создаю тестовые данные...")
        content = """Иванов
Иван
Мужской
01/01/1990
8-912-345-6789
Москва

Петрова
Мария
Женский
15-03-1985
test@mail.ru
Санкт-Петербург"""
        
        with open(input_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        with open(input_file, 'r', encoding='utf-8') as f:
            content = f.read()
    
    # Обрабатываем данные
    profiles = content.strip().split('\n\n')
    results = []
    
    for i, profile in enumerate(profiles, 1):
        lines = [line.strip() for line in profile.split('\n') if line.strip()]
        if len(lines) >= 6:
            print(f"Обрабатываю профиль {i}")
            result = process_profile(lines)
            results.append(result)
    
    # Сохраняем результат
    with open(output_file, 'w', encoding='utf-8') as f:
        for result in results:
            f.write('\n'.join(result) + '\n\n')
    
    print(f"Готово! Результат в {output_file}")
    
    # Показываем результат
    print("\nРезультат обработки:")
    print("=" * 50)
    with open(output_file, 'r', encoding='utf-8') as f:
        print(f.read())

def process_profile(profile):
    """Обрабатывает один профиль"""
    surname, name, gender, date, contact, city = profile[:6]
    
    # Обрабатываем телефон
    if is_phone(contact):
        contact = format_phone(contact)
    elif not is_email(contact):
        contact = '-'
    
    # Обрабатываем город
    if city and not city.startswith('г.'):
        city = f"г. {city}"
    
    # Обрабатываем дату
    if not is_valid_date(date):
        date = '-'
    else:
        date = format_date(date)
    
    return [surname, name, gender, date, contact, city]

def is_phone(text):
    """Проверяет, является ли текст телефоном"""
    if not text:
        return False
    digits = re.sub(r'\D', '', text)
    return len(digits) == 11 and digits.startswith(('7', '8'))

def is_email(text):
    """Проверяет, является ли текст email"""
    if not text:
        return False
    return '@' in text and '.' in text.split('@')[-1]

def is_valid_date(date):
    """Проверяет валидность даты"""
    if not date:
        return False
    return re.match(r'\d{1,2}[/.-]\d{1,2}[/.-]\d{4}', date) is not None

def format_phone(phone):
    """Форматирует телефон"""
    digits = re.sub(r'\D', '', phone)
    if digits.startswith('7'):
        digits = '8' + digits[1:]
    return f"8 ({digits[1:4]}) {digits[4:7]}-{digits[7:9]}-{digits[9:]}"

def format_date(date):
    """Форматирует дату"""
    match = re.match(r'(\d{1,2})[/.-](\d{1,2})[/.-](\d{4})', date)
    if match:
        day, month, year = match.groups()
        return f"{int(day):02d}.{int(month):02d}.{year}"
    return date

if __name__ == "__main__":
    main()