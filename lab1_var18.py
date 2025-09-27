import re
import sys
from datetime import datetime

def read_file(file_path: str) -> str:
    """Чтение содержимого файла"""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        print(f"Ошибка: Файл {file_path} не найден")
        sys.exit(1)
    except Exception as e:
        print(f"Ошибка при чтении файла: {e}")
        sys.exit(1)

def save_to_file(file_path: str, content: str):
    """Сохранение содержимого в файл"""
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(content)
        print(f"Результат сохранен в файл: {file_path}")
    except Exception as e:
        print(f"Ошибка при сохранении файла: {e}")

def is_valid_phone(phone: str) -> bool:
    """Проверка валидности номера телефона"""
    # Удаляем все пробелы, скобки, дефисы для упрощения проверки
    cleaned_phone = re.sub(r'[\s\(\)\-]', '', phone)
    
    # Проверка на 11 цифр и начало с 8 или +7
    if not re.match(r'^(8|\+7)\d{10}$', cleaned_phone):
        return False
    
    # Проверка формата с разделителями
    phone_patterns = [
        r'^8\s?\(\d{3}\)\s?\d{3}[\-\s]?\d{2}[\-\s]?\d{2}$',  # 8 (012) 345-67-89
        r'^8\s?\d{3}[\s\-]?\d{3}[\s\-]?\d{2}[\s\-]?\d{2}$',  # 8 012 345-67-89
        r'^8\d{10}$',  # 80123456789
        r'^\+7\d{10}$'  # +70123456789
    ]
    
    return any(re.match(pattern, phone) for pattern in phone_patterns)

def parse_profiles(content: str) -> list:
    """Разбор анкет из текста"""
    profiles = []
    current_profile = []
    
    for line in content.split('\n'):
        line = line.strip()
        if line and not line.startswith('#'):  # Пропускаем пустые строки и комментарии
            current_profile.append(line)
            # Если собрали 6 строк - это полная анкета
            if len(current_profile) == 6:
                profiles.append(current_profile)
                current_profile = []
    
    return profiles

def find_invalid_phones(profiles: list) -> list:
    """Поиск анкет с некорректными номерами телефонов"""
    invalid_profiles = []
    
    for profile in profiles:
        if len(profile) >= 5:  # Проверяем, что есть поле с телефоном/email
            phone_email_field = profile[4]  # 5-е поле (индекс 4)
            
            # Проверяем, является ли поле номером телефона (а не email)
            if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', phone_email_field):
                # Это не email, значит проверяем как телефон
                if not is_valid_phone(phone_email_field):
                    invalid_profiles.append(profile)
    
    return invalid_profiles

def display_profiles(profiles: list, title: str):
    """Вывод анкет на экран"""
    print(f"\n{title}")
    print("=" * 60)
    
    for i, profile in enumerate(profiles, 1):
        print(f"Анкета #{i}:")
        for j, field in enumerate(profile):
            field_names = ["Фамилия", "Имя", "Пол", "Дата рождения", "Телефон/Email", "Город"]
            if j < len(field_names):
                print(f"  {field_names[j]}: {field}")
        print("-" * 40)

def main():
    # Проверка аргументов командной строки
    if len(sys.argv) != 2:
        print("Использование: python script.py <имя_файла>")
        print("Пример: python script.py data.txt")
        sys.exit(1)
    
    filename = sys.argv[1]
    output_filename = "valid_data.txt"
    
    # Чтение файла
    print(f"Чтение файла: {filename}")
    content = read_file(filename)
    
    # Разбор анкет
    profiles = parse_profiles(content)
    print(f"Найдено анкет: {len(profiles)}")
    
    # Поиск анкет с некорректными телефонами
    invalid_profiles = find_invalid_phones(profiles)
    
    if invalid_profiles:
        # Вывод найденных анкет с некорректными телефонами
        display_profiles(invalid_profiles, "АНКЕТЫ С НЕКОРРЕКТНЫМИ НОМЕРАМИ ТЕЛЕФОНОВ:")
        
        # Создание списка валидных анкет (исключаем невалидные)
        valid_profiles = [profile for profile in profiles if profile not in invalid_profiles]
        
        # Сохранение валидных анкет в новый файл
        valid_content = ""
        for profile in valid_profiles:
            valid_content += "\n".join(profile) + "\n\n"
        
        save_to_file(output_filename, valid_content)
        
        print(f"\nСтатистика:")
        print(f"Всего анкет: {len(profiles)}")
        print(f"Некорректных анкет: {len(invalid_profiles)}")
        print(f"Валидных анкет сохранено: {len(valid_profiles)}")
    else:
        print("Анкет с некорректными номерами телефонов не найдено.")
        # Сохраняем все анкеты, так как все валидны
        save_to_file(output_filename, content)

if __name__ == "__main__":
    main()