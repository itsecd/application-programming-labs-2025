import re
import argparse
from datetime import datetime

def parse_arguments():
    # Парсинг аргументов командной строки
    parser = argparse.ArgumentParser(description='Анализ анкет людей')
    parser.add_argument('filename', type=str, help='Имя файла с данными')
    return parser.parse_args()

def read_file(filename):
    # Чтение файла с данными
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        print(f"Ошибка: Файл {filename} не найден")
        return None
    except Exception as e:
        print(f"Ошибка при чтении файла: {e}")
        return None

def split_profiles(content):
    # Разделение содержимого на отдельные анкеты
    profiles = re.split(r'\n\d+\)\n', content)[1:]  # Пропускаем первый элемент (пустой)
    return profiles

def parse_profile(profile_text):
    # Разбор одной анкеты
    data = {}
    
    # Извлекаем основные поля с помощью регулярных выражений
    fields = {
        'surname': r'Фамилия:\s*([^\n]+)',
        'name': r'Имя:\s*([^\n]+)',
        'gender': r'Пол:\s*([^\n]+)',
        'birth_date': r'Дата рождения:\s*([^\n]+)',
        'contact': r'Номер телефона или email:\s*([^\n]+)',
        'city': r'Город:\s*([^\n]+)'
    }
    
    for field, pattern in fields.items():
        match = re.search(pattern, profile_text)
        if match:
            data[field] = match.group(1).strip()
    
    return data

def is_21st_century(birth_date):
    # Проверка, родился ли человек в 21 веке
    # Регулярное выражение для различных форматов даты
    date_pattern = r'(\d{1,2})[./-](\d{1,2})[./-](\d{2,4})'
    match = re.search(date_pattern, birth_date)
    
    if match:
        day, month, year = match.groups()
        
        # Если год указан двумя цифрами, преобразуем в четыре
        if len(year) == 2:
            year = '20' + year if int(year) <= 23 else '19' + year
        
        year = int(year)
        
        # Проверяем, что год > 2000
        return year > 2000
    
    return False

def process_profiles(profiles):
    # Обработка всех анкет и поиск родившихся в 21 веке
    twenty_first_century_profiles = []
    
    for profile_text in profiles:
        profile = parse_profile(profile_text)
        
        if 'birth_date' in profile and is_21st_century(profile['birth_date']):
            twenty_first_century_profiles.append(profile_text)
    
    return twenty_first_century_profiles

def save_results(profiles, filename='21st_century_profiles.txt'):
    # Сохранение результатов в файл
    if profiles:
        with open(filename, 'w', encoding='utf-8') as output_file:
            for i, profile in enumerate(profiles, 1):
                output_file.write(f"{i})\n{profile}\n")
        return filename
    return None

def print_statistics(profiles):
    # Вывод статистики на экран 
    count = len(profiles)
    print(f"Количество людей, родившихся в 21 веке: {count}")

def main():
    # Парсинг аргументов
    args = parse_arguments()
    
    # Чтение файла
    content = read_file(args.filename)
    if content is None:
        return
    
    # Разделение на анкеты
    profiles = split_profiles(content)
    
    # Обработка анкет
    twenty_first_century_profiles = process_profiles(profiles)
    
    # Вывод статистики
    print_statistics(twenty_first_century_profiles)
    
    # Сохранение результатов
    output_file = save_results(twenty_first_century_profiles)
    if output_file:
        print(f"Анкеты сохранены в файл: {output_file}")

if __name__ == "__main__":
    main()