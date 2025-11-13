import re
import argparse
from datetime import datetime

"""Парсинг аргументов командной строки"""
parser = argparse.ArgumentParser()
parser.add_argument('filename', type=str, help='Название файла с данными')
args = parser.parse_args()

"""Чтение и разделение данных на анкеты"""
with open(args.filename, 'r', encoding='utf-8') as file:
    content = file.read()

profiles = content.split('\n\n')
current_year = datetime.now().year
matching_profiles = []

"""Поиск людей возрастом 30-40 лет"""
for profile in profiles:
    date_match = re.search(r'(\d{1,2})[/.-](\d{1,2})[/.-](\d{4})', profile)

    if date_match:
        day = int(date_match.group(1))
        month = int(date_match.group(2))
        year = int(date_match.group(3))

        """Проверка корректности даты и возраста"""
        if 1900 <= year <= current_year and 1 <= month <= 12 and 1 <= day <= 31:
            age = current_year - year

            if 30 <= age <= 40:
                matching_profiles.append(profile)

"""Вывод результатов и сохранение в файл"""
print(f"Количество людей возрастом от 30 до 40 лет: {len(matching_profiles)}")

with open('profiles_30_40.txt', 'w', encoding='utf-8') as output_file:
    for profile in matching_profiles:
        output_file.write(profile + '\n\n')

print("Анкеты сохранены в файл 'profiles_30_40.txt'")