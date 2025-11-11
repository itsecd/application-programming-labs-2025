import argparse
import re
from typing import List, Dict


def read_file(filename: str) -> str:
 
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"Файл {filename} не найден")
    except IOError as e:
        raise IOError(f"Ошибка чтения файла {filename}: {e}")


def parse_profiles(text: str) -> List[Dict[str, str]]:
  
    profiles = []
    
    profile_blocks = re.split(r'\n\s*\n', text.strip())
    
    for block in profile_blocks:
        lines = [line.strip() for line in block.split('\n') if line.strip()]
        
        if len(lines) >= 6:  
            profile = {
                'surname': lines[0],
                'name': lines[1],
                'gender': lines[2],
                'birth_date': lines[3],
                'contact': lines[4],
                'city': lines[5]
            }
            profiles.append(profile)
    
    return profiles


def is_valid_male(gender: str) -> bool:

    male_patterns = [
        r'^М$', r'^м$', r'^Мужской$', r'^мужской$',
        r'^Мужской', r'^мужской'
    ]
    
    for pattern in male_patterns:
        if re.match(pattern, gender, re.IGNORECASE):
            return True
    
    return False


def count_male_profiles(profiles: List[Dict[str, str]]) -> int:
   
    count = 0
    
    for profile in profiles:
        gender = profile.get('gender', '')
        
        if is_valid_male(gender):
            count += 1
    
    return count


def save_male_profiles(profiles: List[Dict[str, str]], output_filename: str) -> None:
 
    try:
        with open(output_filename, 'w', encoding='utf-8') as file:
            for profile in profiles:
                gender = profile.get('gender', '')
                
                if is_valid_male(gender):
                    file.write(f"{profile['surname']}\n")
                    file.write(f"{profile['name']}\n")
                    file.write(f"{profile['gender']}\n")
                    file.write(f"{profile['birth_date']}\n")
                    file.write(f"{profile['contact']}\n")
                    file.write(f"{profile['city']}\n\n")
    except IOError as e:
        raise IOError(f"Ошибка записи в файл {output_filename}: {e}")


def main() -> None:
   
    parser = argparse.ArgumentParser(description='Обработка анкет людей')
    parser.add_argument('filename', type=str, help='Путь к файлу с анкетами')
    
    args = parser.parse_args()
    
    try:
        text = read_file(args.filename)
        
        profiles = parse_profiles(text)
        
        male_count = count_male_profiles(profiles)
        
        print(f"Количество анкет мужчин: {male_count}")
        
        output_filename = 'male_profiles.txt'
        save_male_profiles(profiles, output_filename)
        print(f"Анкеты мужчин сохранены в файл: {output_filename}")
        
    except FileNotFoundError as e:
        print(f"Ошибка: {e}")
    except IOError as e:
        print(f"Ошибка ввода-вывода: {e}")
    except Exception as e:
        print(f"Неожиданная ошибка: {e}")


if __name__ == '__main__':
    main()