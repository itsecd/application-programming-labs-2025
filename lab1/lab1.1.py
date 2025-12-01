import re
import argparse


def get_args():
    """Получение аргументов из командной строки"""
    parser = argparse.ArgumentParser()
    parser.add_argument("in_file", type=str, help="input file")
    parser.add_argument("out_file", type=str, help="output file")
    return parser.parse_args()


def read_file(filename):
    """Чтение содержимого файла"""
    with open(filename, "r", encoding="utf-8") as f:
        return f.read()

    
def main():
        args = get_args()
        text = read_file(args.in_file)
        print(text)
       
if __name__ == '__main__':
    main()
