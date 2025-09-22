#!/usr/bin/env python3

import re
import argparse


def read_file(filename):
    try:
        with open(filename, "r") as file:
            return file.read()
    except FileNotFoundError:
        print("[!] File not found :(")


def write_file(filename, data):
    count = 1
    with open(filename, "w+") as file:
        file.write("Всего: {}".format(len(data)) + "\n")
        for dat in data:
            file.write(f"{count})\n" + dat + "\n")
            count = count + 1


def args_parse():
    parser = argparse.ArgumentParser(
        prog="Data parser", description="Parsing data from file"
    )
    parser.add_argument("-f", "--file", type=str, help="Parse file")
    parser.add_argument("-o", "--output", type=str, help="Output file")
    return parser.parse_args()


def parse_data(data):
    data = re.split(r"\d\)\s*", data, maxsplit=1)
    parts = [p.strip() for p in re.split(r"\n\d+\)\s*", data[1]) if p.strip()]

    pattern = (
        r"Фамилия:\s*(Иванов[а]*)\s*"
        r"Имя:\s*([А-ЯЁ][а-яё\-]+)\s*"
        r"Пол:\s*(Мужской|М|м|Женский|Ж|ж)\s*"
        r"Дата рождения:\s*(\d{1,2}[./-]\d{1,2}[./-]\d{4})\s*"
        r"Номер телефона или email:\s*((?:\+7|8)[\d\s()\-]{10,}|[A-Za-z0-9._%+-]+@(gmail\.com|yandex\.ru|mail\.ru))\s*"
        r"Город:\s*([А-ЯЁа-яё\- ]+)"
    )

    result = []

    for part in parts:
        matched = re.search(pattern, part)
        if not matched:
            continue
        result.append(part)
    return result


def main():
    args = args_parse()
    text = read_file(args.file)
    parsed = parse_data(text)
    count = 1
    print("Всего: {}".format(len(parsed)))
    for data in parsed:
        print(f"{count})\n" + data)
        count = count + 1
    if args.output:
        write_file(args.output, parsed)


if __name__ == "__main__":
    main()
