import argparse
import re

def read_file(file_name: str) -> str:
    with open(file_name, "r", encoding='utf-8') as file:
        text = file.read()
    return text

def arg_parser() -> str:
    parser = argparse.ArgumentParser()
    parser.add_argument('name', type=str, help='Print Filename')
    arg = parser.parse_args()
    return arg.name

def main():
    try:
        file_to_parse = arg_parser()
        file_content = read_file(file_to_parse)
    except Exception as e:
        print(f"Ошибка: {e}")
    finally:
        print("Программа завершена")

if __name__ == "__main__":
    main()