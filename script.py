import argparse
import re

def parse_arguments():
    """
    Парсинг аргументов командной строки
    """
    parser = argparse.ArgumentParser(description='Поиск дубликатов номеров телефонов в анкетах')
    parser.add_argument('filename', type=str, help='Путь к файлу с данными анкет')
    return parser.parse_args()

def extract_phone_numbers(text):
    """
    Извлечение номеров телефонов из текста с помощью регулярных выражений
    """
    phone_pattern = r'(?:\+7|8)[\s\(\-]*\d{3}[\s\)\-]*\d{3}[\s\-]*\d{2}[\s\-]*\d{2}'
    
    phones = re.findall(phone_pattern, text)
    
    normalized_phones = []
    for phone in phones:
        cleaned = re.sub(r'[^\d+]', '', phone)
        if cleaned.startswith('8') and len(cleaned) == 11:
            cleaned = '+7' + cleaned[1:]
        normalized_phones.append(cleaned)
    
    return normalized_phones

def parse_profiles(text):
    """
    Парсинг анкет из текста
    """
    profiles = []
    current_profile = {}
    
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
            phones = extract_phone_numbers(phone_email)
            if phones:
                current_profile['phone'] = phones[0]
    if current_profile:
        profiles.append(current_profile)
    
    return profiles

def find_duplicate_phones(profiles):
    """
    Поиск анкет с дублирующимися номерами телефонов
    """
    phone_dict = {}
    
    for profile in profiles:
        if 'phone' in profile:
            phone = profile['phone']
            if phone in phone_dict:
                phone_dict[phone].append(profile)
            else:
                phone_dict[phone] = [profile]
    
    duplicates = {phone: profiles for phone, profiles in phone_dict.items() if len(profiles) > 1}
    return duplicates

def main():
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