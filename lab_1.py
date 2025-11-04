import argparse
import re

def parse_arguments()->argparse.Namespace:
    """
    Название файла через аргумент командной строки.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', type=str, help='the name of the file to open')
    return parser.parse_args()

def open_file(args: argparse.Namespace) -> str:
    """
    Открытие файла.
    """
    try:
        with open(args.filename, "r", encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        print(f"Ошибка: Файл {args.filename} не найден")
        exit('1')
    except Exception as e:
        print(f"Ошибка при чтении файла: {e}")
        exit('1')

def extract_surnames(text: str) -> list[str]:
    """
    Приводит текст файла к списку строк вида: Фамилия И.\n
    """
    surnames = re.findall("Фамилия:\s[А-Я][а-я]+\sИмя:\s[А-Я]", text)
    for i in range(0,len(surnames)):
        surnames[i] = surnames[i][9:]
        surnames[i] = re.sub("\sИмя:\s", ' ', surnames[i])+'.\n'
    return surnames

def save_surnames_in_file(name: str, surnames: list[str]) -> int:
    """
    Запись или же перезапись фамилий и имен в файл.
    """
    try:
        with open(name, 'w', encoding='utf-8') as file:
            for surname in surnames:
                file.write(surname)
        print(f"Файл {name} успешно создан/перезаписан")
        return 0
    except Exception as e:
        print(f"Ошибка при сохранении файла: {e}")
        exit(1)
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
