import argparse
import re
import csv
from datetime import datetime


def validate_name(name):
    """Проверка валидности имени и фамилии"""
    # Убираем возможные префиксы типа "Фамилия:"
    clean_name = re.sub(r'^[^:]*:\s*', '', name).strip()
    if re.fullmatch(r'[А-ЯЁ][а-яё]*', clean_name):
        return clean_name
    return '-'


def validate_gender(gender):
    """Проверка валидности пола"""
    clean_gender = re.sub(r'^[^:]*:\s*', '', gender).strip()
    male_patterns = [r'^М$', r'^м$', r'^Мужской$', r'^мужской$']
    female_patterns = [r'^Ж$', r'^ж$', r'^Женский$', r'^женский$']

    for pattern in male_patterns:
        if re.fullmatch(pattern, clean_gender):
            return 'М'
    for pattern in female_patterns:
        if re.fullmatch(pattern, clean_gender):
            return 'Ж'
    return '-'


def validate_birthdate(date_str):
    """Проверка валидности даты рождения"""
    clean_date = re.sub(r'^[^:]*:\s*', '', date_str).strip()

    # Проверяем различные форматы даты
    patterns = [
        r'^(\d{1,2})[/.-](\d{1,2})[/.-](\d{4})$',
        r'^(\d{1,2})[/.-](\d{1,2})[/.-](\d{2})$',
        r'^(\d{1,2})\s+(\d{1,2})\s+(\d{4})$',
        r'^(\d{1,2})\s+(\d{1,2})\s+(\d{2})$'
    ]

    for pattern in patterns:
        match = re.fullmatch(pattern, clean_date)
        if match:
            day, month, year = match.groups()
            if len(year) == 2:
                year = '19' + year  # предполагаем 20 век для двухзначного года

            try:
                # Проверяем, что дата корректна
                birth_date = datetime(int(year), int(month), int(day))
                current_year = datetime.now().year

                # Проверяем диапазон года
                if 1900 <= birth_date.year <= current_year:
                    return f"{int(day):02d}/{int(month):02d}/{year}"
            except ValueError:
                continue
    return '-'


def validate_phone(phone):
    """Проверка валидности номера телефона"""
    clean_phone = re.sub(r'^[^:]*:\s*', '', phone).strip()

    # Убираем все пробелы, скобки и дефисы для проверки
    digits_only = re.sub(r'[\s\(\)\-\.]', '', clean_phone)

    # Проверяем основные форматы
    patterns = [
        r'^8\d{10}$',  # 80123456789
        r'^\+7\d{10}$'  # +71234567890
    ]

    for pattern in patterns:
        if re.fullmatch(pattern, digits_only):
            # Форматируем номер в стандартный вид
            if digits_only.startswith('8'):
                formatted = f"8 ({digits_only[1:4]}) {digits_only[4:7]}-{digits_only[7:9]}-{digits_only[9:]}"
            else:
                formatted = f"+7 ({digits_only[2:5]}) {digits_only[5:8]}-{digits_only[8:10]}-{digits_only[10:]}"
            return formatted

    return '-'


def validate_email(email):
    """Проверка валидности email"""
    clean_email = re.sub(r'^[^:]*:\s*', '', email).strip()
    pattern = r'^[A-Za-z0-9._%+-]{1,64}@(gmail\.com|mail\.ru|yandex\.ru)$'
    if re.fullmatch(pattern, clean_email):
        return clean_email
    return '-'


def validate_city(city):
    """Проверка валидности города"""
    clean_city = re.sub(r'^[^:]*:\s*', '', city).strip()
    # Убираем "г." и пробелы для проверки
    clean_city_no_prefix = re.sub(r'^г\.\s*', '', clean_city).strip()
    if re.fullmatch(r'[А-ЯЁA-Z][а-яёa-z\s\-]*', clean_city_no_prefix):
        return clean_city
    return '-'


def parse_person_data(lines):
    """Парсинг данных одного человека из списка строк"""
    person = {}

    for line in lines:
        line = line.strip()
        if line.startswith('Фамилия:'):
            person['last_name'] = line
        elif line.startswith('Имя:'):
            person['first_name'] = line
        elif line.startswith('Пол:'):
            person['gender'] = line
        elif line.startswith('Дата рождения:'):
            person['birthdate'] = line
        elif line.startswith('Номер телефона или email:'):
            person['contact'] = line
        elif line.startswith('Город:'):
            person['city'] = line

    return person if len(person) == 6 else None


def process_contact_info(contact):
    """Определение типа контактной информации и валидация"""
    clean_contact = re.sub(r'^[^:]*:\s*', '', contact).strip()

    # Проверяем, является ли контакт email
    if '@' in clean_contact:
        email = validate_email(contact)
        return {'phone': '-', 'email': email}
    else:
        phone = validate_phone(contact)
        return {'phone': phone, 'email': '-'}


def main():
    # Парсинг аргументов командной строки
    parser = argparse.ArgumentParser(description='Обработка анкет людей из файла')
    parser.add_argument('filename', type=str, help='Путь к файлу с данными')
    args = parser.parse_args()

    try:
        # Чтение файла
        with open(args.filename, 'r', encoding='utf-8') as file:
            lines = file.readlines()

        # Обработка данных
        people_data = []
        current_person = []

        for line in lines:
            line = line.strip()
            if line and not re.match(r'^\d+\)$', line):  # если строка не пустая и не номер анкеты
                current_person.append(line)
            elif not line and current_person:  # пустая строка - разделитель между анкетами
                person_data = parse_person_data(current_person)
                if person_data:
                    # Валидация данных
                    validated_person = {
                        'Фамилия': validate_name(person_data['last_name']),
                        'Имя': validate_name(person_data['first_name']),
                        'Пол': validate_gender(person_data['gender']),
                        'Дата рождения': validate_birthdate(person_data['birthdate']),
                        'Город': validate_city(person_data['city'])
                    }

                    # Обработка контактной информации
                    contact_info = process_contact_info(person_data['contact'])
                    validated_person['Номер телефона'] = contact_info['phone']
                    validated_person['Почта'] = contact_info['email']

                    people_data.append(validated_person)
                current_person = []

        # Обработка последней анкеты, если файл не заканчивается пустой строкой
        if current_person:
            person_data = parse_person_data(current_person)
            if person_data:
                validated_person = {
                    'Фамилия': validate_name(person_data['last_name']),
                    'Имя': validate_name(person_data['first_name']),
                    'Пол': validate_gender(person_data['gender']),
                    'Дата рождения': validate_birthdate(person_data['birthdate']),
                    'Город': validate_city(person_data['city'])
                }

                contact_info = process_contact_info(person_data['contact'])
                validated_person['Номер телефона'] = contact_info['phone']
                validated_person['Почта'] = contact_info['email']

                people_data.append(validated_person)

        # Сохранение в CSV файл
        output_filename = 'processed_data.csv'
        with open(output_filename, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['Фамилия', 'Имя', 'Пол', 'Дата рождения', 'Номер телефона', 'Почта', 'Город']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            for person in people_data:
                writer.writerow(person)

        # Вывод результата на экран
        print(f"Обработано анкет: {len(people_data)}")
        print(f"Результат сохранен в файл: {output_filename}")
        print("\nПервые 10 обработанных анкет:")
        print("-" * 100)
        for i, person in enumerate(people_data[:10], 1):
            print(f"Анкета {i}:")
            for key, value in person.items():
                print(f"  {key}: {value}")
            print()

        # Статистика по некорректным данным
        invalid_count = {
            'Фамилия': sum(1 for p in people_data if p['Фамилия'] == '-'),
            'Имя': sum(1 for p in people_data if p['Имя'] == '-'),
            'Пол': sum(1 for p in people_data if p['Пол'] == '-'),
            'Дата рождения': sum(1 for p in people_data if p['Дата рождения'] == '-'),
            'Номер телефона': sum(1 for p in people_data if p['Номер телефона'] == '-'),
            'Почта': sum(1 for p in people_data if p['Почта'] == '-'),
            'Город': sum(1 for p in people_data if p['Город'] == '-')
        }

        print("\nСтатистика некорректных данных:")
        print("-" * 40)
        for field, count in invalid_count.items():
            print(f"{field}: {count} некорректных записей")

    except FileNotFoundError:
        print(f"Ошибка: Файл '{args.filename}' не найден.")
    except Exception as e:
        print(f"Произошла ошибка: {e}")


if __name__ == "__main__":
    main()