import argparse
import re

def parse_arguments():
    '''Название файла через аргумент командной строки'''
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', type=str, help='the name of the file to open')
    return parser.parse_args()

def open_file(args):
    '''открытие файла'''
    with open(args.filename, "r", encoding='utf-8') as file:
        return file.read()

def extract_surnames(text):
    '''Приводит текст файла к списку строк вида: Фамилия И.\n'''
    surnames = re.findall("Фамилия:\s[А-Я][а-я]+\sИмя:\s[А-Я]", text)
    for i in range(0,len(surnames)):
        surnames[i] = surnames[i][9:]
        surnames[i] = re.sub("\sИмя:\s", ' ', surnames[i])+'.\n'
    return surnames

def save_surnames_in_file(name, surnames):
    '''запись или же перезапись фамилий и имен в файл'''
    with open(name, 'w', encoding='utf-8') as file:
        for i in range(0, len(surnames)):
            file.write(surnames[i])

def main():
    args = parse_arguments()
    text = open_file(args)
    surnames = extract_surnames(text)
    surnames.sort()
    print('input filename (format: format.txt):')
    file_to_open = str(input())
    save_surnames_in_file(file_to_open, surnames)

if __name__ == '__main__':
    main()
