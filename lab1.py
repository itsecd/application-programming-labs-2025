import argparse
import re


def parse_ankets(file_path: str) -> list:
    """
    Читает анкеты из файла.
    """
    ankets = []
    current_anket = {}
    field_names = [
        "last_name", "first_name", "middle_name",
        "birth_date", "email", "city"
    ]
    field_count = 0

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                line = line.strip()

                if not line and current_anket:
                    if field_count == 6:
                        ankets.append(current_anket)
                    current_anket = {}
                    field_count = 0
                    continue

                if line:
                    if field_count == 0:
                        current_anket = {field_names[0]: line}
                    elif field_count < 6:
                        current_anket[field_names[field_count]] = line
                    field_count += 1

        if current_anket and field_count == 6:
            ankets.append(current_anket)

    except FileNotFoundError:
        print(f"Ошибка: Файл {file_path} не найден")
        exit(1)

    return ankets


def check_email(contact: str) -> str:
    """
    Проверяет, похожа ли строка на email.
    """
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.(com|ru|org|net)$"
    if re.match(pattern, contact):
        return contact
    else:
        raise ValueError("Неверный email")


def find_duplicates(anket_list: list) -> dict:
    """
    Находит одинаковые email.
    """
    email_groups = {}

    for anket in anket_list:
        email = anket.get("email", "")
        try:
            valid_email = check_email(email)
            if valid_email not in email_groups:
                email_groups[valid_email] = []
            email_groups[valid_email].append(anket)
        except ValueError:
            continue

    duplicates = {}
    for email, group in email_groups.items():
        if len(group) > 1:
            duplicates[email] = group

    return duplicates


def show_results(duplicates: dict) -> None:
    """
    Показывает дубликаты email.
    """
    if not duplicates:
        print("Все email уникальны.")
        return
    print("Анкеты с дубликатами email:")
    print("-" * 30)
    for email, anket_group in duplicates.items():
        print(f"\nEmail: {email}")
        for i, anket in enumerate(anket_group, 1):
            print(f"  Анкета {i}:")
            print(f"    Контакт: {anket.get('email', '')}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Проверка уникальности email в анкетах.")
    parser.add_argument('file_path', type=str, help="Путь к файлу data.txt")
    args = parser.parse_args()
    try:
        ankets = parse_ankets(args.file_path)
        duplicates = find_duplicates(ankets)
        show_results(duplicates)
    except (FileNotFoundError, ValueError) as error:
        print(f"Ошибка: {error}")


if __name__ == "__main__":
    main()
