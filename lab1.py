import argparse
import re

def parse_arguments() -> str:
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file", type=str, help="input file path")
    args = parser.parse_args()
    return args.input_file

def read_file(input_file: str) -> str:

    print(f"Reading file: {input_file}")
    with open(input_file, 'r', encoding='utf-8') as file:
        return file.read()

def main() -> None:
    try:
        input_file = parse_arguments()
        data = read_file(input_file)
        print(data)
        
    except Exception as exc:
        print(f"Возникла ошибка: {exc}")

if __name__ == "__main__":
    main()