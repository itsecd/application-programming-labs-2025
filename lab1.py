import argparse
import re

def read_file(file_name: str) -> str:
    with open(file_name, "r", encoding='utf-8') as file:
        text = file.read()
    return text

def write_file(file_name: str, content: str):
    with open(file_name, "w", encoding='utf-8') as file:
        file.write(content)

def arg_parser() -> str:
    parser = argparse.ArgumentParser()
    parser.add_argument('name', type=str, help='Print Filename')
    arg = parser.parse_args()
    return arg.name

def parse_profiles(data: str):
    profiles = []
    raw_profiles = data.strip().split('\n\n')
    
    for profile in raw_profiles:
        lines = profile.strip().split('\n')
        profile_data = {}
        
        for line in lines:
            if ':' in line:
                key, value = line.split(':', 1)
                key = key.strip().lower()
                value = value.strip()
                
                if key == 'фамилия':
                    profile_data['last_name'] = value
                elif key == 'имя':
                    profile_data['first_name'] = value
                elif key == 'пол':
                    profile_data['gender'] = value
                elif 'дата' in key:
                    profile_data['birth_date'] = value
                elif 'телефон' in key or 'email' in key:
                    profile_data['contact'] = value
                elif key == 'город':
                    profile_data['city'] = value
        
        if len(profile_data) >= 6:
            profiles.append(profile_data)
    return profiles

def fix_names(profiles):
    has_errors = False
    for profile in profiles:
        if profile['last_name'] and not profile['last_name'][0].isupper():
            old_name = profile['last_name']
            profile['last_name'] = old_name.capitalize()
            has_errors = True
            print(f"Исправлена фамилия: {old_name} -> {profile['last_name']}")
        
        if profile['first_name'] and not profile['first_name'][0].isupper():
            old_name = profile['first_name']
            profile['first_name'] = old_name.capitalize()
            has_errors = True
            print(f"Исправлено имя: {old_name} -> {profile['first_name']}")
    
    return has_errors

def create_fixed_content(profiles):
    content_parts = []
    for profile in profiles:
        profile_lines = [
            f"Фамилия: {profile['last_name']}",
            f"Имя: {profile['first_name']}",
            f"Пол: {profile['gender']}",
            f"Дата рождения: {profile['birth_date']}",
            f"Номер телефона или email: {profile['contact']}",
            f"Город: {profile['city']}"
        ]
        content_parts.append('\n'.join(profile_lines))
    
    return '\n\n'.join(content_parts)

def main():
    try:
        file_to_parse = arg_parser()
        file_content = read_file(file_to_parse)
        profiles = parse_profiles(file_content)
        has_errors = fix_names(profiles)
        if has_errors:
            fixed_content = create_fixed_content(profiles)
            output_file = "fixed__" + file_to_parse
            write_file(output_file, fixed_content)
            print(f"Исправленный файл сохранен как: {output_file}")
        else:
            print("Все имена и фамилии корректны")
    except Exception as e:
        print(f"Ошибка: {e}")
    finally:
        print("Программа завершена")

if __name__ == "__main__":
    main()