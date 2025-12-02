import re
import sys
from datetime import datetime

def is_valid_date(date_str):
    """Проверка валидности даты в различных форматах"""
    date_patterns = [
        r'^(\d{1,2})[/.-](\d{1,2})[/.-](\d{4})$',
    ]
    
    for pattern in date_patterns:
        match = re.match(pattern, date_str)
        if match:
            day, month, year = match.groups()
            
            try:
                day = int(day)
                month = int(month)
                year = int(year)
                
                current_year = datetime.now().year
                if year < 1900 or year > current_year:
                    return False
                
                datetime(year, month, day)
                
                if year == current_year:
                    today = datetime.now()
                    if datetime(year, month, day) > today:
                        return False
                
                return True
            except ValueError:
                return False
    
    return False

def extract_data_from_line(line):
    """Извлечение данных из строк вида 'Фамилия: Иванов' или '1) Фамилия: Иванов'"""
    # Убираем нумерацию в начале строки (например, "1) ")
    line = re.sub(r'^\d+\)\s*', '', line.strip())
    
    # Ищем паттерн "Поле: Значение"
    match = re.match(r'^([^:]+):\s*(.+)$', line)
    if match:
        field, value = match.groups()
        return field.strip(), value.strip()
    return None, None

def parse_person_data(profile_lines):
    """Извлечение фамилии и даты рождения из анкеты человека"""
    surname = None
    birth_date = None
    
    for line in profile_lines:
        field, value = extract_data_from_line(line)
        
        if field and value:
            if field.lower() == 'фамилия':
                surname = value
            elif field.lower() == 'дата рождения':
                birth_date = value
    
    # Проверяем, что получили оба значения
    if surname and birth_date:
        # Проверяем, что фамилия начинается с заглавной буквы
        if not surname[0].isupper():
            return None
        
        # Проверяем валидность даты
        if is_valid_date(birth_date):
            return (surname, birth_date)
    
    return None

def calculate_age(birth_date_str):
    """Вычисление возраста из строки даты рождения"""
    date_pattern = r'^(\d{1,2})[/.-](\d{1,2})[/.-](\d{4})$'
    match = re.match(date_pattern, birth_date_str)
    
    if match:
        day, month, year = map(int, match.groups())
        birth_date = datetime(year, month, day)
        today = datetime.now()
        
        age = today.year - birth_date.year
        
        if (today.month, today.day) < (birth_date.month, birth_date.day):
            age -= 1
        
        return age
    
    return 0

def main():
    if len(sys.argv) < 2:
        print("Использование: python3 script.py <имя_файла>")
        print("Пример: python3 script.py data.txt")
        sys.exit(1)
    
    filename = sys.argv[1]
    
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Разделяем на анкеты - каждая анкета начинается с номера
        profiles = []
        current_profile = []
        
        lines = content.strip().split('\n')
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            # Если строка начинается с цифры и скобки (например, "1)"), это начало новой анкеты
            if re.match(r'^\d+\)', line):
                if current_profile:
                    profiles.append(current_profile)
                current_profile = [line]
            else:
                current_profile.append(line)
        
        # Добавляем последнюю анкету
        if current_profile:
            profiles.append(current_profile)
        
        person_data = []
        
        for profile_lines in profiles:
            data = parse_person_data(profile_lines)
            if data:
                person_data.append(data)
        
        if not person_data:
            print("В файле не найдено валидных данных.")
            return
        
        # Сортируем по возрасту (от старшего к младшему)
        person_data.sort(key=lambda x: calculate_age(x[1]), reverse=True)
        
        # Формируем список в формате "Фамилия: дата рождения"
        result_list = [f"{surname}: {birth_date}" for surname, birth_date in person_data]
        
        output_filename = "sorted_by_age.txt"
        with open(output_filename, 'w', encoding='utf-8') as output_file:
            for item in result_list:
                output_file.write(item + '\n')
        
        print(f"✓ Данные успешно обработаны")
        print(f"✓ Найдено {len(person_data)} валидных записей из {len(profiles)} анкет")
        print(f"✓ Результат сохранен в файл: '{output_filename}'")
        
        print("\n" + "="*60)
        print("Отсортированный список (от старшего к младшему):")
        print("="*60)
        for i, item in enumerate(result_list[:20], 1):  # Показываем первые 20 записей
            surname, date = item.split(": ")
            age = calculate_age(date)
            print(f"{i:3}. {surname:20} {date:15} (возраст: {age} лет)")
        
        if len(result_list) > 20:
            print(f"\n... и еще {len(result_list) - 20} записей")
            
    except FileNotFoundError:
        print(f"✗ Ошибка: Файл '{filename}' не найден.")
        print(f"  Убедитесь, что файл находится в той же папке, что и скрипт.")
    except Exception as e:
        print(f"✗ Произошла ошибка: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()