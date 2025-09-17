#Найти всех людей с фамилиями, оканчивающимися на "ов(а)". Выведите их количество на экран и сохраните анкеты в новый файл.
import argparse
import re

#parser = argparse.ArgumentParser()
#parses.add_argumet('data', type=str, help = "File with anket")
#agrs = parser.parse_args()

import re

def parse_file():
    #Читает файл data.txt и извлекает анкеты
    try:
        with open('data.txt', 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        print("Error: file data.txt not found.")
        exit(1)
    except Exception as e:
        print(f"Error pri chtenii file: {e}")
        exit(1)
    
    entries = []
    lines = content.strip().split('\n')
    current_entry = {}
    
    for line in lines:
        line = line.strip()
        if re.match(r'^\d+\)', line):  # Начало новой анкеты
            if current_entry:
                entries.append(current_entry)
            current_entry = {}
        elif ':' in line:
            key, value = line.split(':', 1)
            key = key.strip()
            value = value.strip()
            current_entry[key] = value
    
    if current_entry:
        entries.append(current_entry)
    
    return entries

def surname_ends_with_ov_or_ova(surname):
    #Проверяет, оканчивается ли фамилия на 'ов' или 'ова'
    return bool(re.match(r'^.*ов(?:а)?$', surname, re.IGNORECASE))

def main():
    # Читаем только data.txt — жёстко зашито
    entries = parse_file()
    
    # Фильтруем по фамилии
    matching_entries = []
    for entry in entries:
        if 'Фамилия' in entry and surname_ends_with_ov_or_ova(entry['Фамилия']):
            matching_entries.append(entry)
    
    # Выводим количество
    count = len(matching_entries)
    print(count)
    
    # Сохраняем в новый файл
    with open('filtered_data.txt', 'w', encoding='utf-8') as f:
        for i, entry in enumerate(matching_entries, 1):
            f.write(f"{i})\n")
            for key, value in entry.items():
                f.write(f"{key}: {value}\n")
            f.write("\n")

if __name__ == "__main__":
    main()