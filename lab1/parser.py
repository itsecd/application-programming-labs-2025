#!/usr/bin/env python3

import re
import argparse


def read_file(filename: str) -> str | None:
    try:
        with open(filename, "r") as file:
            return file.read()
    except FileNotFoundError:
        print("[!] File not found :(")


def write_file(filename: str, data: list[str]):
    """Запись данных в файл с именем filename"""
    count = 1
    with open(filename, "w+") as file:
        file.write("Всего: {}".format(len(data)) + "\n")
        for dat in data:
            file.write(f"{count})\n" + dat + "\n")
            count = count + 1


def args_parse() -> argparse.Namespace:
    """Парсинг аргументов в список"""
    parser = argparse.ArgumentParser(
        prog="Data parser", description="Parsing data from file"
    )
    parser.add_argument("-f", "--file", type=str, help="Parse file")
    parser.add_argument("-o", "--output", type=str, help="Output file")
    return parser.parse_args()


def parse_data(data: str) -> list[str]:
    """Дробление данных в элементы списка, парсинг"""
    data = re.split(r"\d\)\s*", data, maxsplit=1)
    parts = [p.strip() for p in re.split(r"\n\d+\)\s*", data[1]) if p.strip()]

    pattern = r"Фамилия:\s*(Иванов[а]{0,1})\s*"

    result = []

    for part in parts:
        matched = re.search(pattern, part)
        if not matched:
            continue
        result.append(part)
    return result


def main() -> None:
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
