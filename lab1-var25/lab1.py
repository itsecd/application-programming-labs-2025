import re
import sys
import argparse
from datetime import datetime

def read_file(filename):
    """Чтение файла и возвращение списка строк"""
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            return file.readlines()
    except FileNotFoundError:
        print(f"Файл {filename} не найден")
        sys.exit(1)
    except Exception as e:
        print(f"Ошибка при чтении файла: {e}")
        sys.exit(1)

def parse_profiles(lines):
    """Парсинг анкет из списка строк"""
    profiles = []
    current_profile = {}
    
    for line in lines:
        line = line.strip()
        
        # Пропускаем пустые строки
        if not line:
            continue
            
        # Определяем, начинается ли новая анкета (по номеру в скобках)
        if re.match(r'^\d+\)$', line):
            if current_profile:  # Сохраняем предыдущую анкету
                profiles.append(current_profile)
            current_profile = {}
            continue
            
        # Определяем тип данных по содержанию строки
        if 'surname' not in current_profile:
            # Извлекаем фамилию (убираем "Фамилия: ")
            surname = re.sub(r'^Фамилия:\s*', '', line)
            current_profile['surname'] = surname
        elif 'name' not in current_profile:
            # Извлекаем имя (убираем "Имя: ")
            name = re.sub(r'^Имя:\s*', '', line)
            current_profile['name'] = name
        elif 'gender' not in current_profile:
            # Извлекаем пол (убираем "Пол: ")
            gender = re.sub(r'^Пол:\s*', '', line)
            current_profile['gender'] = gender
        elif 'birth_date' not in current_profile:
            # Извлекаем дату рождения (убираем "Дата рождения: ")
            birth_date = re.sub(r'^Дата рождения:\s*', '', line)
            current_profile['birth_date'] = birth_date
        elif 'contact' not in current_profile:
            # Извлекаем контакт (убираем "Номер телефона или email: ")
            contact = re.sub(r'^Номер телефона или email:\s*', '', line)
            current_profile['contact'] = contact
        elif 'city' not in current_profile:
            # Извлекаем город (убираем "Город: ")
            city = re.sub(r'^Город:\s*', '', line)
            current_profile['city'] = city
    
    # Добавляем последнюю анкету
    if current_profile:
        profiles.append(current_profile)
        
    return profiles

def validate_name(name):
    """Проверка валидности имени/фамилии - начинаются с заглавной буквы"""
    pattern = r'^[A-ZА-ЯЁ][a-zа-яё\-]*$'
    return bool(re.match(pattern, name))

def sort_profiles_by_names(profiles):
    """Сортировка анкет по фамилиям и именам в алфавитном порядке"""
    # Фильтруем только валидные фамилии и имена
    valid_profiles = []
    invalid_profiles = []
    
    for profile in profiles:
        if (validate_name(profile['surname']) and 
            validate_name(profile['name'])):
            valid_profiles.append(profile)
        else:
            invalid_profiles.append(profile)
    
    # Сортируем по фамилии, затем по имени
    sorted_profiles = sorted(valid_profiles, 
                           key=lambda x: (x['surname'].lower(), x['name'].lower()))
    
    return sorted_profiles, invalid_profiles

def save_to_new_file(profiles, original_filename):
    """Сохранение результата в новый файл с сохранением структуры"""
    # Создаем имя нового файла
    if '.' in original_filename:
        name_part = original_filename.rsplit('.', 1)[0]
        new_filename = f"{name_part}_sorted.txt"
    else:
        new_filename = f"{original_filename}_sorted.txt"
    
    try:
        with open(new_filename, 'w', encoding='utf-8') as file:
            for i, profile in enumerate(profiles, 1):
                file.write(f"{i})\n")
                file.write(f"Фамилия: {profile['surname']}\n")
                file.write(f"Имя: {profile['name']}\n")
                file.write(f"Пол: {profile['gender']}\n")
                file.write(f"Дата рождения: {profile['birth_date']}\n")
                file.write(f"Номер телефона или email: {profile['contact']}\n")
                file.write(f"Город: {profile['city']}\n\n")
        
        print(f"Результат сохранен в файл: {new_filename}")
        return new_filename
    except Exception as e:
        print(f"Ошибка при сохранении файла: {e}")
        return None

def analyze_invalid_profiles(invalid_profiles):
    """Анализ невалидных профилей"""
    print("\nАнализ невалидных профилей:")
    for profile in invalid_profiles:
        issues = []
        if not validate_name(profile['surname']):
            issues.append("фамилия")
        if not validate_name(profile['name']):
            issues.append("имя")
        
        print(f"  {profile['surname']} {profile['name']} - невалидные: {', '.join(issues)}")

def main():
    # Создание парсера аргументов командной строки
    parser = argparse.ArgumentParser(description='Сортировка анкет по фамилиям и именам')
    parser.add_argument('filename', type=str, help='Название файла с анкетами')
    
    # Парсинг аргументов
    args = parser.parse_args()
    filename = args.filename
    
    # Чтение файла
    print("Чтение файла...")
    lines = read_file(filename)
    
    # Парсинг анкет
    print("Парсинг анкет...")
    profiles = parse_profiles(lines)
    
    print(f"Найдено анкет: {len(profiles)}")
    
    # Сортировка по фамилиям и именам
    print("Сортировка анкет...")
    sorted_profiles, invalid_profiles = sort_profiles_by_names(profiles)
    
    print(f"Валидных анкет для сортировки: {len(sorted_profiles)}")
    print(f"Невалидных анкет: {len(invalid_profiles)}")
    
    # Вывод результата на экран
    print("\nПервые 20 отсортированных анкет (Фамилия Имя):")
    for i, profile in enumerate(sorted_profiles[:20], 1):
        print(f"{i:2}. {profile['surname']} {profile['name']}")
    
    if len(sorted_profiles) > 20:
        print(f"... и еще {len(sorted_profiles) - 20} анкет")
    
    # Анализ невалидных профилей
    if invalid_profiles:
        analyze_invalid_profiles(invalid_profiles)
    
    # Сохранение в новый файл
    print("\nСохранение результата...")
    saved_file = save_to_new_file(sorted_profiles, filename)
    
    if saved_file:
        print(f"Всего сохранено {len(sorted_profiles)} анкет")

if __name__ == "__main__":
    main()