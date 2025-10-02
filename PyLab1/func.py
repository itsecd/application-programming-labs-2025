import argparse
import io
import re


def get_args() -> str:
    """
    keep filename of terminal
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", type=str)
    args = parser.parse_args()
    return args.filename


def intput_file(filename: str) -> str:
    """
    parsing first file
    """
    try:
        file = open(filename, "r")
        print(f"File {filename} ready to work")
        text = file.read()
        file.close()
        return text
    except FileNotFoundError:
        print("Sorry, this file impossible to detect")
        return ""


def is_correct_name(data: str) -> bool:
    """
    cheking name of one human
    """
    name = r"Имя: [А-Я][а-я]*"
    if re.search(name, data):
        return True
    return False


def is_correct_surname(data: str) -> bool:
    """
    cheking surname of one human
    """
    surname = r"Фамилия: [А-Я][а-я]*"
    if re.search(surname, data):
        return True
    return False


def data_change_surname(human: str) -> str:
    """
    correction surname of one human
    """
    human = human.split("\n")
    human[1] = human[1].title()  # заглавление первой буквы фамилии
    answer = ""
    for str in human:
        answer += (str+"\n")
    return answer


def data_change_name(human: str) -> str:
    """
    correction name of one human
    """
    human = human.split("\n")
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
