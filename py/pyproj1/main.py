import argparse
import re

from datetime import datetime


def factor(human: list) -> bool:
    return  name(human[0]) and name(human[1]) and gender(human[2]) and city(human[5]) and date(human[3]) and num_mail(human[4])


def name(text: str) -> bool:
    if re.fullmatch(r'^[А-Я][а-я]+',text.split(' ')[1]):
        return True
    return False


def gender(text: str) -> bool:
    if re.fullmatch(r'(М|м|Мужской|мужской|Ж|ж|Женский|женский)', text.split(' ')[1]):
        return True
    return False


def date(text: str) -> bool:
    text = text.split(' ')[2:]
    text = ' '.join(text)
    if re.fullmatch(r'(\d{1,2}(/\d{1,2}/|-\d{1,2}-|\.\d{1,2}\.)20\d{2})', text):
        text = re.split(r'[-/.]', text)
        day, month, year = int(text[0]), int(text[1]), int(text[2])

        # месяца
        if month > 12:
            return False

        # дни
        d31 = [1, 3, 5, 7, 8, 10, 12]
        d30 = [4, 6, 9, 11]

        if month in d31 and day > 31:
            return False
        if month in d30 and day > 30:
            return False
        if month == 2 and day > 28:
            return False
        if month == 2 and (year % 4 == 0 or year % 100 == 0) and day > 29:
            return False

        blank_date = datetime(year=year, month=month, day=day)
        current = datetime.now()
        if blank_date >= current:
            return False

        return True
    return False


def num_mail(text: str) -> bool:
    text = text.split(' ')[4:]
    text = ' '.join(text)
    numb_pat = r'(\+7|8)(\s?\d{3}\s?|\s\(\d{3}\)\s)\d{3}(\s?\d{2}\s?|-\d{2}-)\d{2}'
    email_pat = r'[a-zA-Z\d\-.+%_]{1,64}@(yandex\.ru|gmail\.com|mail\.ru)'
    if re.fullmatch(numb_pat, text) or re.fullmatch(email_pat, text):
        return True
    return False


def city(text: str) -> bool:
    text = text.split(' ')[1:]
    text = ' '.join(text)
    if re.search(r'(г\.\s[А-Я][а-я]+|[А-Я][а-я]+)', text):
        return True
    return False


def read_new_file(filename: str) -> list[str]:
    with open(filename, "r", encoding="utf-8") as data:
        return data.readlines()


def write_new_file(filename: str, string: str) -> None:
    with open(filename, "w", encoding="utf-8") as data:
        data.write(string)


def fill_blanks(counter: int, questionaty: list[str]) -> str:
    result = ""
    result += str(counter) + ')' + '\n'
    for l in questionaty:
        result += l + "\n"
    result += '\n'
    return result


def most_work(whole_text: list[str], write_file_name: str) -> int:
    result_work = ""
    blank = []
    number = 0
    for line in whole_text:
        if line == '\n' or not line:
            if blank and factor(blank):
                number += 1
                result_work += fill_blanks(number, blank)
            blank = []
            continue
        if re.fullmatch(r'\d+\)\n', line):
            continue
        blank.append(line.strip())
    write_new_file(write_file_name, result_work)
    return number


def main():
    try:
        parser = argparse.ArgumentParser(description='Фильтрация файла с анкетами')
        parser.add_argument('input_file', type=str, help='Имя входного файла')
        parser.add_argument('output_file', type=str, help='Имя получаемого файла')

        args = parser.parse_args()

        all_lines = read_new_file(args.input_file)

        mass = most_work(all_lines, args.output_file)

        print(mass)

    except FileNotFoundError:
        print(f"Ошибка: Читаемый файл не найден.")
        return []
    except UnicodeDecodeError:
        print(f"Ошибка: Некорректная кодировка в читаемом файле.")
        return []
    except PermissionError:
        print(f"Ошибка: Нет прав на запись в файла.")

if __name__ == "__main__":
    main()