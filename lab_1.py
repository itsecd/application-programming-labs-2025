import argparse
import re

'''Название файла через аргумент командной строки'''
parser = argparse.ArgumentParser()
parser.add_argument('filename', type=str, help='the name of the file to open')
args = parser.parse_args()

'''открытие файла'''
with open(args.filename, "r", encoding='utf-8') as file:
    text = file.read()

'''обработка фамилий и имен'''
surnames = re.findall("Фамилия:\s[А-Я][а-я]+\sИмя:\s[А-Я]", text)
for i in range(0,len(surnames)):
    surnames[i] = surnames[i][9:]
    surnames[i] = re.sub("\sИмя:\s", ' ', surnames[i])+'.\n'
surnames.sort()

'''запись и создание, или же перезапись фамилий и имен в новый файл'''
with open("surnames.txt",'w',encoding='utf-8') as file:
    for i in range(0, len(surnames)):
        file.write(surnames[i])
