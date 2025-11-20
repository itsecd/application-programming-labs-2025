import argparse
import re
import sys
from typing import List, Tuple

def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', type=str, help='Имя файла с анкетами')
    return parser.parse_args()

def read_file(filename: str) -> str:  
   try:
        with open(filename, 'r', encoding='utf-8') as file:
            return file.read()        
   except IOError as e:   
        raise IOError(f"Ошибка чтения файла '{filename}': {e}")

def parse_profiles(text: str) -> List[Tuple[str, str, str, str, str, str]]:
    profiles = []
    profile_blocks = re.split(r'\n\d+\)', text)
    
    for block in profile_blocks:
        if not block.strip():
            continue
        surname_match = re.search(r'Фамилия:\s*(.+)', block)
        name_match = re.search(r'Имя:\s*(.+)', block)
        gender_match = re.search(r'Пол:\s*(.+)', block)
        birth_match = re.search(r'Дата рождения:\s*(.+)', block)
        contact_match = re.search(r'Номер телефона или email:\s*(.+)', block)
        city_match = re.search(r'Город:\s*(.+)', block)
        
        if all([surname_match, name_match, gender_match, birth_match, contact_match, city_match]):
            surname = surname_match.group(1).strip()
            name = name_match.group(1).strip()
            gender = gender_match.group(1).strip()
            birth_date = birth_match.group(1).strip()
            contact = contact_match.group(1).strip()
            city = city_match.group(1).strip()
            
            profiles.append((surname, name, gender, birth_date, contact, city))
    
    return profiles

def is_valid_male(gender: str) -> bool:
    male_patterns = [
        r'^М$',
        r'^Мужской$',
        r'^Мужской',
        r'^М '
    ]
    
    for pattern in male_patterns:
        if re.search(pattern, gender.strip(), re.IGNORECASE):
            return True
    
    return False

def filter_male_profiles(profiles: List[Tuple[str, str, str, str, str, str]]) -> List[Tuple[str, str, str, str, str, str]]:
    male_profiles = []
    
    for profile in profiles:
        surname, name, gender, birth_date, contact, city = profile
        
        if is_valid_male(gender):
            male_profiles.append(profile)
    
    return male_profiles

def save_profiles_to_file(profiles: List[Tuple[str, str, str, str, str, str]], filename: str) -> None:
    try:
        with open(filename, 'w', encoding='utf-8') as file:
            for i, profile in enumerate(profiles, 1):
                surname, name, gender, birth_date, contact, city = profile
                file.write(f"{i})\n")
                file.write(f"Фамилия: {surname}\n")
                file.write(f"Имя: {name}\n")
                file.write(f"Пол: {gender}\n")
                file.write(f"Дата рождения: {birth_date}\n")
                file.write(f"Номер телефона или email: {contact}\n")
                file.write(f"Город: {city}\n\n")
    except IOError as e:
        raise IOError(f"Ошибка записи в файл '{filename}': {e}")

def main() -> None:
    try:
        args = parse_arguments()
        file_content = read_file(args.filename)
        profiles = parse_profiles(file_content)
        male_profiles = filter_male_profiles(profiles)
        
        print(f"Количество анкет мужчин: {len(male_profiles)}")

        output_filename = "male_profiles.txt"
        save_profiles_to_file(male_profiles, output_filename)
        print(f"Анкеты сохранены в файл: {output_filename}")

    except FileNotFoundError as e:
        print(f"Ошибка: {e}", file=sys.stderr)
        sys.exit(1)
    except IOError as e:
        print(f"Ошибка ввода-вывода: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Неожиданная ошибка: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
  main()
