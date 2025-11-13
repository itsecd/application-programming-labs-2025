import argparse
import re


def capitalize_name(name: str) -> str:
    """Приводит имя или фамилию к виду с заглавной первой буквой."""
    return name.capitalize()


def fix_lines(lines: list[str]) -> list[str]:
    """Исправляет регистр значений в строках 'Имя: ...' и 'Фамилия: ...'."""
    fixed_lines = []
    pattern = re.compile(r"^(Имя|Фамилия):\s*(.+)$")
    for line in lines:
        stripped = line.rstrip("\n")
        match = pattern.match(stripped)
        if match:
            key, value = match.groups()
            corrected = f"{key}: {capitalize_name(value)}\n"
            fixed_lines.append(corrected)
        else:
            fixed_lines.append(line if line.endswith("\n") else line + "\n")
    return fixed_lines


def read_file(filename: str) -> list[str]:
    """Читает текстовый файл в кодировке UTF-8 и возвращает список строк."""
    try:
        with open(filename, "r", encoding="utf-8") as f_in:
            return f_in.readlines()
    except FileNotFoundError:
        raise FileNotFoundError(f"Файл '{filename}' не найден.")
    except Exception as e:
        raise Exception(f"Ошибка при чтении файла: {e}")


def generate_output_filename(input_file: str) -> str:
    """Создаёт имя выходного файла, добавляя префикс 'fixed_' к исходному."""
    return "fixed_" + input_file


def save_file(filename: str, lines: list[str]) -> None:
    """Записывает список строк в файл с кодировкой UTF-8."""
    try:
        with open(filename, "w", encoding="utf-8") as f_out:
            f_out.writelines(lines)
    except Exception as e:
        raise Exception(f"Ошибка при записи в файл '{filename}': {e}")


def process_file(input_file: str) -> None:
    """Обрабатывает анкетный файл: читает, исправляет и сохраняет результат."""
    lines = read_file(input_file)
    fixed_lines = fix_lines(lines)
    output_file = generate_output_filename(input_file)
    save_file(output_file, fixed_lines)
    print(f"Исправленные данные сохранены в {output_file}")


def parse_arguments() -> argparse.Namespace:
    """Парсит аргумент командной строки --filename (обязательный)."""
    parser = argparse.ArgumentParser(
        description="Исправление регистра имён и фамилий в файле анкет."
    )
    parser.add_argument(
        "-f",
        "--filename",
        type=str,
        help="Имя входного файла с анкетами",
        required=True,
    )
    return parser.parse_args()


def main() -> None:
    """Точка входа: запускает обработку с обработкой исключений."""
    args = parse_arguments()
    try:
        process_file(args.filename)
    except Exception as e:
        print(f"Ошибка: {e}")


if __name__ == "__main__":
    main()
