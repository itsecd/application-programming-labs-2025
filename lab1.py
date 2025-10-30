import argparse
import re

def parse_ankets(file_path):
    """
    Читает анкеты из файла.
    """
    ankets = []
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
        current_anket = {}
        for line in lines:
            line = line.strip()
            if not line and current_anket:
                if len(current_anket) == 6:
                    ankets.append(current_anket)
                current_anket = {}
            elif line and not current_anket:
                current_anket = {'last_name': line}
            else:
                current_anket['next_field'] = line
        if current_anket and len(current_anket) == 6:
            ankets.append(current_anket)
    except FileNotFoundError:
        raise FileNotFoundError(f"Файл {file_path} не найден")
    return ankets

def check_email(contact):
    """
    Проверяет, похожа ли строка на email.
    """
    if '@' in contact and ('.com' in contact or '.ru' in contact):
        return contact
    raise ValueError("Неверный email")

def find_duplicates(anket_list):
    """
    Находит одинаковые email.
    """
    email_dict = {}
    for anket in anket_list:
        try:
            email = check_email(anket.get('next_field', ''))
            if email not in email_dict:
                email_dict[email] = []
            email_dict[email].append(anket)
        except ValueError:
            pass
    return {email: group for email, group in email_dict.items() if len(group) > 1}

def show_results(duplicates):
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
            print(f"    Контакт: {anket.get('next_field', '')}")

def main():
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
