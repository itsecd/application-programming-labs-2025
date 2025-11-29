import argparse
import re
import sys
from typing import List


def read_file(file_path: str) -> str:
    """
    Читает содержимое файла file_path в строку
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"Файл '{file_path}' не найден")
    except PermissionError:
        raise PermissionError(f"Нет прав для чтения файла '{file_path}'")
    except UnicodeDecodeError:
        raise UnicodeDecodeError("Ошибка кодировки файла."
        )


def write_file(file_path: str, data: List[str]) -> None:
    """
    Записывает содержимое списка List[str] в файл file_path
    """
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write("\n\n".join(data))
    except PermissionError:
        raise PermissionError(f"Нет прав для записи в файл '{file_path}'")
    except IOError as e:
        raise IOError(f"Ошибка записи в файл '{file_path}': {e}")


def extract_female_names_starting_with_a(content: str) -> List[str]:
    """
    Создает список анкет с женскими именами, начинающимися с буквы А
    """
    if not content or not content.strip():
        raise ValueError("Файл пуст")

    valid_female_sex = [
        'Ж',
        'ж',
        'Женский',
        'женский'
    ]

    try:
        forms = re.split(r"\n\s*\n", content.strip())
    except re.error as e:
        raise ValueError(f"Ошибка при чтении анкет: {e}")

    valid_forms = []
    for form_text in forms:
        is_female = False
        name_starts_with_A = False

        for line in form_text.split('\n'):
            if 'Имя:' in line:
                name_value = line.split('Имя:')[1].strip() 
                if re.match(r'А\w*', name_value):
                    name_starts_with_A = True
            elif 'Пол:' in line:
                sex_value = line.split('Пол:')[1].strip() 
                if any(sex_check == sex_value for sex_check in valid_female_sex):
                    is_female = True
        if is_female and name_starts_with_A:
            valid_forms.append(form_text) 
    return valid_forms


def count_forms(forms: List[str]) -> int:
    """
    Считает количество анкет в списке
    """
    return len(forms)


def main() -> None:
    try:
        parser = argparse.ArgumentParser()

        parser.add_argument(
        'input_file',
        type=str,
        help='Путь к входному файлу с анкетами'
    )

        parser.add_argument(
        'output_file',
        type=str,
        help='Путь к выходному файлу для сохранения результата'
    )

        args = parser.parse_args()
        content = read_file(args.input_file)
        valid_forms = extract_female_names_starting_with_a(content)
        valid_form_count = count_forms(valid_forms)

        print(f"Количество подходящих анкет: {valid_form_count}")

        write_file(args.output_file, valid_forms)
    except Exception as e:
        print(f"Ошибка: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()