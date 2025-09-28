import argparse
import re


parser = argparse.ArgumentParser()  # создание экземпляра парсера
parser.add_argument('filename', type=str, help='filename')  # добавление позиционного аргумента командной строки
args = parser.parse_args() # парсинг аргументов
try:
    file = open(args.filename)
except FileNotFoundError:
    print(f"Sorry, {args.filename} dont found!!!")
print(f"File {args.filename} is parsed!")  # использование полученного значения аргумента
