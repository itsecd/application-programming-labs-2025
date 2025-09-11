import re


def read_file() -> str:
    filename = "C:/Users/elisa/Downloads/data.txt"
    with open(filename, "r", encoding='utf-8') as file:
        text = file.read()
    return text

def main():
    read_file()

if __name__ == "__main__":
    main()