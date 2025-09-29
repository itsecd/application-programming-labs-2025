import re
import argparse
from pathlib import Path
from typing import List, Tuple


def read_file(file_path: Path) -> str:
    """
    Чтение содержимого файла.
    
    Args:
        file_path: Путь к файлу для чтения
        
    Returns:
        Содержимое файла в виде строки
        
    Raises:
        FileNotFoundError: Если файл не найден
        IOError: При ошибках чтения файла
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"Файл {file_path} не найден")
    except Exception as e:
        raise IOError(f"Ошибка при чтении файла {file_path}: {e}")


def save_to_file(file_path: Path, content: str) -> None:
    """
    Сохранение содержимого в файл.
    
    Args:
        file_path: Путь к файлу для сохранения
        content: Содержимое для сохранения
    """
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(content)


def is_likely_email(value: str) -> bool:
    """
    Определяет, похоже ли значение на email.
    
    Args:
        value: Значение для проверки
        
    Returns:
        True если значение похоже на email, иначе False
    """
    return bool(re.search(r'[a-zA-Z]', value))


def is_valid_phone(phone: str) -> bool:
    """
    Проверка валидности номера телефона.
    
    Args:
        phone: Номер телефона для проверки
        
    Returns:
        True если номер телефона валиден, иначе False
    """
    phone = phone.strip()
    cleaned_phone = re.sub(r'[\s\(\)\-\.]', '', phone)
    
    if not re.match(r'^(8|\+7)\d{10}$', cleaned_phone):
        return False
    
    phone_patterns = [
        r'^8\s?\(\d{3}\)\s?\d{3}[\-\s]?\d{2}[\-\s]?\d{2}$',
        r'^8\s?\d{3}[\s\-]?\d{3}[\s\-]?\d{2}[\s\-]?\d{2}$',
        r'^8\d{10}$',
        r'^8\s?\d{3}\s?\d{3}\s?\d{2}\s?\d{2}$',
        r'^\+7\s?\(\d{3}\)\s?\d{3}[\-\s]?\d{2}[\-\s]?\d{2}$',
        r'^\+7\s?\d{3}[\s\-]?\d{3}[\s\-]?\d{2}[\s\-]?\d{2}$',
        r'^\+7\d{10}$',
        r'^\+7\s?\d{3}\s?\d{3}\s?\d{2}\s?\d{2}$',
    ]
    
    return any(re.match(pattern, phone) for pattern in phone_patterns)


def parse_profiles(content: str) -> List[List[str]]:
    """
    Разбор анкет из текста.
    
    Args:
        content: Текст для разбора
        
    Returns:
        Список анкет, где каждая анкета - список строк
    """
    profiles = []
    lines = [line.strip() for line in content.split('\n') if line.strip()]
    
    i = 0
    while i < len(lines):
        if re.match(r'^\d+\)$', lines[i]):
            profile = lines[i:i+7]
            if len(profile) == 7:
                profiles.append(profile)
            i += 7
        else:
            i += 1
    
    return profiles


def find_invalid_phones(profiles: List[List[str]]) -> List[List[str]]:
    """
    Поиск анкет с некорректными номерами телефонов.
    
    Args:
        profiles: Список анкет для проверки
        
    Returns:
        Список анкет с некорректными телефонами
    """
    invalid_profiles = []
    
    for profile in profiles:
        for line in profile:
            if line.startswith('Номер телефона или email:'):
                value = line.split(':', 1)[1].strip()
                
                if is_likely_email(value):
                    break
                elif not is_valid_phone(value):
                    invalid_profiles.append(profile)
                break
    
    return invalid_profiles


def display_invalid_profiles(profiles: List[List[str]]) -> None:
    """Вывод анкет с некорректными телефонами на экран."""
    print("\nАНКЕТЫ С НЕКОРРЕКТНЫМИ НОМЕРАМИ ТЕЛЕФОНОВ:")
    print("=" * 60)
    
    for i, profile in enumerate(profiles, 1):
        print(f"АНКЕТА #{i}:")
        for field in profile:
            print(f"  {field}")
        print("-" * 60)


def process_profiles(input_file: Path, output_file: Path) -> Tuple[int, int, int]:
    """
    Основная функция обработки профилей.
    
    Args:
        input_file: Путь к входному файлу
        output_file: Путь к выходному файлу
        
    Returns:
        Кортеж (всего_анкет, некорректных_анкет, валидных_анкет)
    """
    content = read_file(input_file)
    profiles = parse_profiles(content)
    invalid_profiles = find_invalid_phones(profiles)
    valid_profiles = [p for p in profiles if p not in invalid_profiles]
    
    if invalid_profiles:
        display_invalid_profiles(invalid_profiles)
        
        print("\nДЕТАЛИ НАЙДЕННЫХ ОШИБОК:")
        for i, profile in enumerate(invalid_profiles, 1):
            for line in profile:
                if line.startswith('Номер телефона или email:'):
                    phone = line.split(':', 1)[1].strip()
                    print(f"{i}. Некорректный номер телефона: {phone}")
                    break
        
        valid_content = "\n\n".join("\n".join(p) for p in valid_profiles)
        save_to_file(output_file, valid_content)
    else:
        save_to_file(output_file, content)
        print("Анкет с некорректными номерами телефонов не найдено.")
    
    return len(profiles), len(invalid_profiles), len(valid_profiles)


def main() -> None:
    """Основная функция программы."""
    parser = argparse.ArgumentParser(
        description='Проверка анкет на корректность номеров телефонов'
    )
    parser.add_argument('input_file', type=Path, help='Путь к входному файлу с анкетами')
    parser.add_argument('output_file', type=Path, help='Путь к выходному файлу')
    
    args = parser.parse_args()
    
    try:
        print(f"Чтение файла: {args.input_file}")
        total, invalid, valid = process_profiles(args.input_file, args.output_file)
        
        print(f"\nСТАТИСТИКА ОБРАБОТКИ:")
        print(f"Всего анкет: {total}")
        print(f"Некорректных: {invalid}")
        print(f"Валидных: {valid}")
        print(f"Результат сохранен в: {args.output_file}")
        
    except FileNotFoundError as e:
        print(f"Ошибка: {e}")
    except IOError as e:
        print(f"Ошибка ввода-вывода: {e}")
    except Exception as e:
        print(f"Неожиданная ошибка: {e}")


if __name__ == "__main__":
    main()