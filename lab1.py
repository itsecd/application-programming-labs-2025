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
print(f"Всего анкет найдено: {len(profiles)}")