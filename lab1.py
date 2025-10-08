import argparse
from typing import List


def capitalize_name(name: str) -> str:
    """Приводит первую букву к заглавной, остальные — к строчным."""
    return name.capitalize()


def fix_lines(lines: List[str]) -> List[str]:
    """Исправляет регистр в строках 'Фамилия:' и 'Имя:'."""
    fixed = []
    for line in lines:
        if "Фамилия:" in line or "Имя:" in line:
            parts = line.rsplit(": ", 1)
            if len(parts) == 2:
                key, value = parts[0], parts[1].strip()
                line = f"{key}: {capitalize_name(value)}\n"
        fixed.append(line)
    return fixed


def process_file(input_file: str, output_file: str = "fixed_data.txt") -> None:
    """Читает входной файл, исправляет имена/фамилии, записывает результат."""
    try:
        with open(input_file, "r", encoding="utf-8") as f:
            lines = f.readlines()
        fixed_lines = fix_lines(lines)
        with open(output_file, "w", encoding="utf-8") as f:
            f.writelines(fixed_lines)
        print(f"Исправленные данные сохранены в {output_file}")
    except FileNotFoundError:
        print(f"Ошибка: файл '{input_file}' не найден.")
        raise
    except Exception as e:
        print(f"Произошла ошибка при обработке файла: {e}")
        raise


def parse_args() -> argparse.Namespace:
    """Парсит аргументы командной строки."""
    parser = argparse.ArgumentParser(
        description="Исправление регистра имён и фамилий в файле анкет."
    )
    parser.add_argument("filename", help="Имя входного файла с анкетами")
    return parser.parse_args()


def main() -> None:
    """Основная функция программы."""
    args = parse_args()
    process_file(args.filename)


if __name__ == "__main__":
    try:
        main()
    except Exception:
        pass