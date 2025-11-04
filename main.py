import argparse
import re

def read_and_parse_persons(file_path: str) -> list:
    """
    Читает файл и извлекает только валидные email из анкет.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            raw_text: str = f.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"Файл '{file_path}' не найден.")

    persons: list = []
    blocks: list = raw_text.strip().split('\n\n')

    for block in blocks:
        lines: list = [line.strip() for line in block.splitlines() if line.strip()]
        if len(lines) < 6:
            continue

        if lines[0].endswith(')'):
            lines = lines[1:]

        def get_field(line: str, prefix: str) -> str:
            return line[len(prefix):].strip() if line.startswith(prefix) else ""

        contact: str = get_field(lines[4], "Номер телефона или email:")

        email: str = parse_contact(contact)
        if email is None:
            continue

        persons.append({
            "email": email,
            "raw_data": block
        })
    return persons

def parse_contact(contact: str) -> str:
    """
    Проверяет, является ли строка валидным email на разрешённых доменах.
    """
    contact_clean: str = contact.strip()
    pattern: str = r'^[A-Za-z0-9._%+-]{1,64}@(gmail\.com|mail\.ru|yandex\.ru)$'
    if re.fullmatch(pattern, contact_clean):
        return contact_clean
    return None

def find_and_print_duplicate_emails(persons: list) -> None:
    """
    Находит и выводит анкеты с дублирующимися email-адресами.
    """
    email_to_persons: dict = {}

    for person in persons:
        email: str = person["email"]
        if email not in email_to_persons:
            email_to_persons[email] = []
        email_to_persons[email].append(person)

    duplicates_found: bool = False

    for email, persons_list in email_to_persons.items():
        if len(persons_list) > 1:
            duplicates_found = True
            print(f"Email: {email}\n")
            for person in persons_list:
                print(person["raw_data"], "\n")

    if not duplicates_found:
        print("Дубликатов email не найдено.")

def main() -> None:

    parser: argparse.ArgumentParser = argparse.ArgumentParser(description="Поиск дубликатов email в файле анкет.")
    parser.add_argument('filename', type=str, help='Имя файла с анкетами (например, data.txt)')
    args: argparse.Namespace = parser.parse_args()

    try:
        persons: list = read_and_parse_persons(args.filename)
        find_and_print_duplicate_emails(persons)
    except Exception as e:
        print(f"Ошибка: {e}")

if __name__ == '__main__':
    main()