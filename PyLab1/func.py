import argparse
import io
import re


def get_args() -> str:
    """
    keep filenames of terminal
    """
    filenames=[]
    parser = argparse.ArgumentParser()
    parser.add_argument("old_filename", type=str)
    parser.add_argument("new_filename", type=str)
    args = parser.parse_args()
    filenames.append(args.old_filename)
    filenames.append(args.new_filename)
    return filenames


def intput_file(filename: str) -> str:
    """
    parsing file
    """
    try:
        file = open(filename, "r", encoding="utf-8")
        print(f"File {filename} ready to work")
        text = file.read()
        file.close()
        return text
    except FileNotFoundError:
        print("Sorry, this file impossible to detect")
        return ""


def is_correct_name_or_surname(data: str) -> int:
    """
    cheking name and surname of one human
    """
    cnt=0
    surname = r"Фамилия: [А-Я][а-я]*"
    name = r"Имя: [А-Я][а-я]*"
    if not re.search(name, data):
        cnt+=1
    if not re.search(surname, data):
        cnt+=1
    return cnt


def data_change_surname_and_name(human: str) -> str:
    """
    correction surname and name of one human
    """
    human = human.split("\n")
    human[1] = human[1].title()  # заглавление первой буквы фамилии
    human[2] = human[2].title()  # заглавление первой буквы имени
    answer = ""
    for str in human:
        answer += (str+"\n")
    return answer


def output_file(file: io.TextIOWrapper, human: str) -> None:
    """
    information of one human push to new file
    """
    file.write(human)
    file.write("\n")
