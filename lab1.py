import argparse
import re
import sys


def parse_args() -> argparse.Namespace:
    """
    Получает путь к файлу
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('path', type=str, help='Path to file (Путь к файлу)')
    return parser.parse_args()


def read_file(path : str) -> str:
    """
    Чтение из файла
    """
    try:
        with open(path, "r", encoding="utf-8") as file:
            return file.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"Файл не найден: {path}")
    


def split_forms(data: str) -> list[str]:
    """
    Функция - разделение на формы
    """
    return data.split("\n\n")


def filter_forms_by_email(forms: list[str]) -> tuple[list[str], list[str]]:
    """
    Деление на почты
    """
    try:
        email_pattern = r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}'
        with_email = [form for form in forms if re.search(email_pattern, form)]
        without_email = [form for form in forms if not re.search(email_pattern, form)]
        return with_email, without_email
    except re.error as error:
        raise ValueError(f"Ошибка в выражении: {error}")


def save_forms_to_file(forms: list[str], filename: str) -> None:
    """
    Сохраняет в файл
    """
    try:
        with open(filename, "w", encoding="utf-8") as file:
            file.write("\n\n".join(forms))
    except OSError as error:
        raise OSError(f"Ошибка записи в файл: {error}")


def main() -> None:
    try:
        args = parse_args()
        data = read_file(args.path)
        forms = split_forms(data)
        form_with_mail, form_without_mail = filter_forms_by_email(forms)

        print("Без почты:")
        for trash in form_without_mail:
            print("\n" + trash)

        save_forms_to_file(form_with_mail, "good_file.txt")

        print(type(args))
    except FileNotFoundError as error:
        print(f"Ошибка {error}", file=sys.stderr)
        sys.exit(1)
    except PermissionError as error:
        print(f"Ошибка доступа к файлу: {error}", file=sys.stderr)
        sys.exit(1)
    except Exception as error:
        print(f"Произошла ошибка: {error}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()