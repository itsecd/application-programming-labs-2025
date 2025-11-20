import argparse
import re


def parse_arguments():
    """Парсит аргументы командной строки"""
    parser = argparse.ArgumentParser(description='Поиск людей по имени в анкетах')
    parser.add_argument("file", help="Путь к файлу с анкетами")
    return parser.parse_args()


def read_profiles(filename):
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


def parse_profile(record):
    """Парсит одну анкету и извлекает данные"""
    lines = record.split('\n')
    profile = {}
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        # Пробуем найти поле в формате "Поле: значение"
        match = re.match(r'^(\w+)[:\s]+(.+)$', line, re.IGNORECASE)
        if match:
            field = match.group(1).lower()
            value = match.group(2).strip()
            
            if field in ['фамилия', 'surname']:
                profile['surname'] = value
            elif field in ['имя', 'name']:
                profile['name'] = value
            elif field in ['пол', 'gender']:
                profile['gender'] = value
            elif field in ['дата', 'birth', 'date']:
                profile['birth_date'] = value
            elif field in ['телефон', 'phone', 'email', 'контакт', 'contact']:
                profile['contact'] = value
            elif field in ['город', 'city']:
                profile['city'] = value
        else:
            # Если формат не "Поле: значение", пробуем определить поле по порядку
            if 'surname' not in profile:
                profile['surname'] = line
            elif 'name' not in profile:
                profile['name'] = line
            elif 'gender' not in profile:
                profile['gender'] = line
            elif 'birth_date' not in profile:
                profile['birth_date'] = line
            elif 'contact' not in profile:
                profile['contact'] = line
            elif 'city' not in profile:
                profile['city'] = line
    
    return profile


def find_people_by_name(records, target_name):
    """Ищет людей по имени (регистронезависимо)"""
    matching_profiles = []
    
    for record in records:
        profile = parse_profile(record)
        name = profile.get('name', '')
        
        # Проверяем совпадение имени (регистронезависимо)
        if name and name.lower() == target_name.lower():
            matching_profiles.append(profile)
    
    return matching_profiles


def save_profiles_to_file(profiles, output_filename):
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


def main():
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
