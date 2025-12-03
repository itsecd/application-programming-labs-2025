import argparse
import re
from typing import List, Dict, Optional


def parse_arguments() -> argparse.Namespace:
    """Парсит аргументы командной строки"""
    parser = argparse.ArgumentParser(description='Поиск людей по имени в анкетах')
    parser.add_argument("file", help="Путь к файлу с анкетами")
    return parser.parse_args()


def read_profiles(filename: str) -> List[str]:
    """Читает анкеты из файла"""
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Разделяем на анкеты по двойному переносу строки
        records = []
        blocks = content.split("\n\n")
        
        for block in blocks:
            cleaned_block = block.strip()
            if cleaned_block:
                records.append(cleaned_block)
                
        return records
                
    except FileNotFoundError:
        raise FileNotFoundError(f"Файл {filename} не найден")
    except Exception as e:
        raise Exception(f"Ошибка при чтении файла: {e}")


def parse_profile(record: str) -> Dict[str, str]:
    """Парсит одну анкету и извлекает данные"""
    lines = record.split('\n')
    profile: Dict[str, str] = {}
    
    # Словарь для сопоставления полей
    field_mapping = {
        'фамилия': 'surname', 'surname': 'surname',
        'имя': 'name', 'name': 'name',
        'пол': 'gender', 'gender': 'gender',
        'дата': 'birth_date', 'birth': 'birth_date', 'date': 'birth_date',
        'телефон': 'contact', 'phone': 'contact', 'email': 'contact', 
        'контакт': 'contact', 'contact': 'contact',
        'город': 'city', 'city': 'city'
    }
    
    # Порядок полей для случая без формата "Поле: значение"
    field_order = ['surname', 'name', 'gender', 'birth_date', 'contact', 'city']
    field_index = 0
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        # Пробуем найти поле в формате "Поле: значение"
        match = re.match(r'^(\w+)[:\s]+(.+)$', line, re.IGNORECASE)
        if match:
            field_key = match.group(1).lower()
            value = match.group(2).strip()
            
            # Используем словарь для сопоставления полей
            if field_key in field_mapping:
                profile[field_mapping[field_key]] = value
        else:
            # Если формат не "Поле: значение", заполняем по порядку
            if field_index < len(field_order):
                profile[field_order[field_index]] = line
                field_index += 1
    
    return profile


def find_people_by_name(records: List[str], target_name: str) -> List[Dict[str, str]]:
    """Ищет людей по имени (регистронезависимо)"""
    matching_profiles: List[Dict[str, str]] = []
    
    for record in records:
        profile = parse_profile(record)
        name = profile.get('name', '')
        
        # Проверяем совпадение имени (регистронезависимо)
        if name and name.lower() == target_name.lower():
            matching_profiles.append(profile)
    
    return matching_profiles


def save_profiles_to_file(profiles: List[Dict[str, str]], output_filename: str) -> None:
    """Сохраняет найденные анкеты в файл"""
    try:
        with open(output_filename, 'w', encoding='utf-8') as file:
            for profile in profiles:
                file.write(f"Фамилия: {profile.get('surname', '')}\n")
                file.write(f"Имя: {profile.get('name', '')}\n")
                file.write(f"Пол: {profile.get('gender', '')}\n")
                file.write(f"Дата рождения: {profile.get('birth_date', '')}\n")
                file.write(f"Контакт: {profile.get('contact', '')}\n")
                file.write(f"Город: {profile.get('city', '')}\n")
                file.write("\n")
                
    except Exception as e:
        raise Exception(f"Ошибка при сохранении файла: {e}")


def main() -> None:
    """Главная функция программы"""
    try:
        args = parse_arguments()
        
        # Читаем анкеты
        records = read_profiles(args.file)
        
        if not records:
            print("Не удалось загрузить анкеты из файла")
            return
        
        print(f"Загружено анкет: {len(records)}")
        
        # Получаем имя для поиска
        target_name = input("Введите имя для поиска: ").strip()
        
        if not target_name:
            print("Имя не может быть пустым")
            return
        
        # Ищем людей
        matching_profiles = find_people_by_name(records, target_name)
        
        # Выводим результаты
        print(f"\nРезультаты поиска:")
        print(f"Людей с именем '{target_name}': {len(matching_profiles)}")
        
        # Сохраняем найденных
        if matching_profiles:
            output_filename = f"people_{target_name}.txt"
            save_profiles_to_file(matching_profiles, output_filename)
            
            print(f"Найденные анкеты сохранены в файл: {output_filename}")
        else:
            print("Люди с таким именем не найдены.")
            
    except FileNotFoundError as e:
        print(f"Ошибка: {e}")
    except Exception as e:
        print(f"Произошла ошибка: {e}")


if __name__ == "__main__":
    main()
