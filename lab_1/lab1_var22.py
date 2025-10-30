import re
import argparse
from typing import List, Tuple

def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file", type=str, help="Имя файла с исходными данными")
    parser.add_argument("-o", "--output_file", type=str, required=True, help="Имя выходного файла")
    return parser.parse_args()

def read_file(filename: str) -> str:
    try:
        with open(filename, 'r', encoding="utf-8") as file:
            return file.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"Файл '{filename}' не был найден")
    
def extract_last_name_phone(data: str) -> List[Tuple[str, str]]:
    pattern = r"Фамилия:\s*([^\n0-9]+)\s*(?:.*?\n)*?Номер телефона или email:\s*([\+\d\-\s\(\)]+)(?=\s*\n)"
    return re.findall(pattern, data, re.IGNORECASE)

def normalize_phone(phone: str) -> str:
    phone = phone.strip()
    digits = re.sub(r"[^\d+]", "", phone)
    
    if digits.startswith("+7"):
        digits = "8" + digits[2:]
    elif not digits.startswith("8"):
        return ""
    
    digits = re.sub(r"\D", "", digits)
    
    if len(digits) == 11:
        return digits
    else:
        return ""
def create_output_list(data: List[Tuple[str, str]]) -> List[str]:
    output = []
    for last_name, phone in data:
        norm_phone = normalize_phone(phone)
        if norm_phone:
            output.append(f"{last_name.strip()}: {norm_phone}")
    return output

def write_to_file(filename: str, lines: List[str]) -> None:
    with open(filename, 'w', encoding='utf-8') as f:
        for line in lines:
            f.write(line + '\n')

def main():
    args = parse_arguments()
    text = read_file(args.input_file)
    extracted = extract_last_name_phone(text)
    output_list = create_output_list(extracted)
    write_to_file(args.output_file, output_list)
    print(f"Результат успешно сохранён в файл {args.output_file}")

if __name__ == "__main__":
    main()
