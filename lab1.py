import argparse
import re

def parse_arguments() -> str:
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file", type=str, help="input file path")
    args = parser.parse_args()
    return args.input_file

def read_file(input_file: str) -> str:
    print(f"Reading file: {input_file}")
    try:
        with open(input_file, 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"File '{input_file}' not found")
    except PermissionError:
        raise PermissionError(f"No permission to read file '{input_file}'")
    except Exception as exc:
        raise Exception(f"Error reading file: {exc}")

def main() -> None:
    try:
        input_file = parse_arguments()
        data = read_file(input_file)
        print(data)
        
    except FileNotFoundError as e:
        print(f"File error: {e}")
    except PermissionError as e:
        print(f"Permission error: {e}") 
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()