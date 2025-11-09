import re
import argparse

def is_valid_phone(phone: str) -> bool:
    '''
    проверка валидности номера телефона с кодом 927
    +7 927 345 67 89
    8 (927) 345-67-89
    89273456789
    '''
    pattern = r'^(?:\+7|8)\s*\(?927\)?[\s-]?\d{3}[\s-]?\d{2}[\s-]?\d{2}$'
    match = re.search(pattern, phone)
    return bool(match)

def extract_records_with_927(text: str) -> list[str]:
    #разделение анкет и выбор тех, где телефон имеет код 927
    
    records = re.split(r'\n\d+\)\n|\n\s*\n', text.strip())
    valid_records = []

    for record in records:
        for line in record.split('\n'):
            if re.match(r'\s*Номер телефона или email:', line):
                contact = line.split(':', 1)[1].strip()
                contact_cleaned = re.sub(r'\s+', ' ', contact)
                if is_valid_phone(contact_cleaned):
                    valid_records.append(record.strip())
                    break

    return valid_records

def read_file(file_name: str) -> str:
    with open(file_name, "r", encoding="utf-8") as file:
        return file.read()

if __name__ == "__main__":
    try:
        text = read_file("test_data.txt")
        records = extract_records_with_927(text)
        print(f"Найдено записей: {len(records)}")
        for i, record in enumerate(records, 1):
            print(f"Запись {i}:\n{record}\n")
    except FileNotFoundError:
        print("Тестовый файл не найден")
