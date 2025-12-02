import argparse
import re

def parse_arguments() -> argparse.Namespace:
    """
    Парсинг аргументов командной строки
    """
    parser = argparse.ArgumentParser(description='Поиск дубликатов номеров телефонов в анкетах')
    parser.add_argument('filename', type=str, help='Путь к файлу с данными анкет')
    return parser.parse_args()

def extract_phone_number(text: str) -> str | None:
    """
    Извлечение номеров телефонов из текста с помощью регулярных выражений
    
    Args:
        text: Текст для поиска номера телефона
        
    Returns:
        Нормализованный номер телефона или None, если номер не найден
    """
    phone_pattern = r'(?:\+7|8)[\s\(\-]*\d{3}[\s\)\-]*\d{3}[\s\-]*\d{2}[\s\-]*\d{2}'
    
    phones = re.search(phone_pattern, text)
    if phones:
        phone = phones.group()
        cleaned = re.sub(r'[^\d+]','',phone)
        if cleaned.startswith('8') and len(cleaned)==11:
            cleaned = '+7' + cleaned[1:]
        return cleaned
    return None

def parse_profiles(text: str) -> list[dict[str, str]]:
    """
    Парсинг анкет из текста
    
    Args:
        text: Текст с данными анкет
        
    Returns:
        Список словарей с данными анкет
    """
    profiles: list[dict[str, str]] = []
    current_profile: dict[str, str] = {}
    
    lines = text.split('\n')
    
    for line in lines:
        line = line.strip()
        
        if line.endswith(')'):
            if current_profile:
                profiles.append(current_profile)
            current_profile = {}
        elif line.startswith('Фамилия:'):
            current_profile['surname'] = line.split(':', 1)[1].strip()
        elif line.startswith('Имя:'):
            current_profile['name'] = line.split(':', 1)[1].strip()
        elif line.startswith('Номер телефона или email:'):
            phone_email = line.split(':', 1)[1].strip()
            current_profile['contact'] = phone_email
            phone = extract_phone_number(phone_email)
            if phone:
                current_profile['phone'] = phone
    if current_profile:
        profiles.append(current_profile)
    
    return profiles

def find_duplicate_phones(profiles: list[dict[str, str]]) -> dict[str, list[dict[str, str]]]:
    """
    Поиск анкет с дублирующимися номерами телефонов
    
    Args:
        profiles: Список анкет для анализа
        
    Returns:
        Словарь где ключи - номера телефонов, значения - списки анкет с этим номером
    """
    phone_dict: dict[str, list[dict[str, str]]] = {}
    
    for profile in profiles:
        if 'phone' in profile:
            phone = profile['phone']
            if phone in phone_dict:
                phone_dict[phone].append(profile)
            else:
                phone_dict[phone] = [profile]
    
    duplicates = {phone: profiles for phone, profiles in phone_dict.items() if len(profiles) > 1}
    return duplicates

def main() -> None:
    """
    Основная функция программы
    """
    args = parse_arguments()
    
    try:
        with open(args.filename, 'r', encoding='utf-8') as file:
            content = file.read()
        profiles = parse_profiles(content)
        duplicates = find_duplicate_phones(profiles)
        if duplicates:
            print("Найдены анкеты с дублирующимися номерами телефонов:")
            print("-" * 40)
            
            for phone, profiles_list in duplicates.items():
                print(f"\nНомер телефона: {phone}")
                print(f"Количество анкет с этим номером: {len(profiles_list)}")
                print("Анкеты:")
                
                for i, profile in enumerate(profiles_list, 1):
                    print(f"  {i}. {profile.get('surname', '')} {profile.get('name', '')}")
                    print(f"     Контакт: {profile.get('contact', '')}")
                
                print("-" * 40)
        
        else:
            print("Дублирующихся номеров телефонов не найдено.")
            
    except FileNotFoundError:
        print(f"Ошибка: Файл '{args.filename}' не найден.")
    except Exception as e:
        print(f"Произошла ошибка: {e}")

if __name__ == "__main__":
    main()