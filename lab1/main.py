import argparse
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
    if not re.fullmatch(r'\b(0?[1-9]|[12][0-9]|3[01])[/\-\.](0?[1-9]|1[0-2])[/\-\.]\d{4}\b', date):
        print(date)
        return False
    else:
        return True

def main():
    parser = argparse.ArgumentParser()  # создание экземпляра парсера
    parser.add_argument('filename', type=str, help='filename')  # добавление позиционного аргумента командной строки
    args = parser.parse_args() # парсинг аргументов
    text = readfile(args.filename)
    text = text.split("\n")
    file = open("correct_date", "w")
    count=0
    for i in range(0,len(text),8):
        if is_correct(text[i+4][15:]) == False:
            count=count+1
            print("yes")
    print(count)





if __name__ == "__main__":
    main()