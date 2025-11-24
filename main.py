import re
import argparse
from typing import List, Tuple


def read_data(filename: str) -> str:
    with open(filename, "r", encoding="utf-8") as f:
        return f.read()


def extract_moscow_residents(content: str) -> List[Tuple[int, str]]:
    pattern = r"(\d+)\)\s*\n(.*?)\nГород:\s*(.*?)(?=\n\d+\)|\Z)"
    matches = re.findall(pattern, content, flags=re.DOTALL)

    moscow_residents = []
    for num_str, body, city in matches:
        norm_city = city.strip()
        if norm_city.startswith("г."):
            norm_city = norm_city[2:].strip()
        if norm_city == "Москва":
            moscow_residents.append((int(num_str), body))
    return moscow_residents


def save_to_file(residents: List[Tuple[int, str]], filename: str) -> None:
    with open(filename, "w", encoding="utf-8") as f:
        for num, body in residents:
            f.write(f"{num})\n{body}\n\n")


def main(input_file: str, output_file: str) -> None:
    content = read_data(input_file)
    moscow_residents = extract_moscow_residents(content)
    count = len(moscow_residents)
    print(f"Количество жителей Москвы: {count}")
    save_to_file(moscow_residents, output_file)
    print(f"😎🤙 Анкеты сохранены в '{output_file}'")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Поиск жителей Москвы в анкетах")
    parser.add_argument(
        "--input",
        default="data.txt",
        help="Имя входного файла (data.txt)"
    )
    parser.add_argument(
        "--output",
        default="moscow_residents.txt",
        help="Имя выходного файла (moscow_residents.txt)"
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    main(args.input, args.output)