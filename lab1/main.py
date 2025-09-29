import argparse
import io
import re

def readfile(filename: str) -> str:
    try:
        file = open(filename, "r")
        print(f"File {filename} is parsed!")
        text = file.read()
        file.close()
        return text
    except FileNotFoundError:
        print(f"Sorry, {filename} dont found!!!")
        return ""

def is_correct(date: str) -> bool:
    if not re.fullmatch(r'(0?[0-9]|[12][0-9]|[3][01])[./-]+(0?[0-9]|[1][012])[./-]+([1][9][0-9]{2}|[2][0][01][0-9]|[2][0][2][0-5])', date):
            return False
    else:
            return True

def print_men(mens: list[str], index:int) -> None:
    for i in range(index,index+8):
            print(mens[i])

def to_file(file: io.TextIOWrapper, index: int, mens: list[str]) -> None:
     for i in range(index, index + 8):
            file.write(mens[i])
            file.write("\n")
     file.write("\n")

def main():
    parser = argparse.ArgumentParser()  # создание экземпляра парсера
    parser.add_argument('filename', type=str, help='filename')  # добавление позиционного аргумента командной строки
    args = parser.parse_args() # парсинг аргументов
    text = readfile(args.filename)
    mens = text.split("\n")
    mens.append("")
    file = open("correct_date.txt", "w")
    for i in range(0,len(mens),8):
        if not is_correct(mens[i+4][15:]):
            print_men(mens,i)
        else:
            to_file(file,i,mens)


if __name__ == "__main__":
    main()