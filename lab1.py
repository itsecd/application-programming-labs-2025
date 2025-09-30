import argparse
import re

def read_file(file_name: str) -> str:
    with open(file_name, "r", encoding='utf-8') as file:
        text = file.read()
    return text

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

def main():
    try:
        file_to_parse = arg_parser()
        file_content = read_file(file_to_parse)
        profiles = parse_profiles(file_content)
    except Exception as e:
        print(f"Ошибка: {e}")
    finally:
        print("Программа завершена")

if __name__ == "__main__":
    main()