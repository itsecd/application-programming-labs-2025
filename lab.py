import re
import argparse
from typing import List, Optional

def is_valid_surname(surname: str) -> bool:

    return bool(re.fullmatch(r'[А-ЯЁ][а-яё]*', surname))


def normalize_phone(raw: str) -> Optional[str]:

    digits = re.sub(r'\D', '', raw)
    if len(digits) == 11 and (digits.startswith('8') or digits.startswith('7')):
        if digits.startswith('7'):
            digits = '8' + digits[1:]
        return f"8 ({digits[1:4]}) {digits[4:7]}-{digits[7:9]}-{digits[9:11]}"
    return None


def is_email(contact: str) -> bool:

    email_pattern = re.compile(r'^[a-zA-Z0-9._%+-]+@(?:gmail\.com|mail\.ru|yandex\.ru)$')
    return bool(email_pattern.match(contact.strip()))


def parse_blocks(content: str) -> List[str]:

    return re.findall(r'Фамилия:.*?(?=\n\s*Фамилия:|\Z)', content, re.DOTALL)


def process_block(block: str) -> Optional[str]:

    lines = [line.strip() for line in block.split('\n') if line.strip()]
    data = {}
    for line in lines:
        if ':' in line:
            key, val = line.split(':', 1)
            data[key.strip()] = val.strip()

    surname = data.get("Фамилия", "")
    contact = data.get("Номер телефона или email", "")

    if not is_valid_surname(surname):
        return None
    if is_email(contact):
        return None

    normalized = normalize_phone(contact)
    if normalized:
        return f"{surname}: {normalized}"
    return None


def main() -> None:

    parser = argparse.ArgumentParser(
        description="Обрабатывает файл с анкетами: оставляет только валидные фамилии с телефонами."
    )
    parser.add_argument(
        "input_file",
        help="Путь к входному файлу с анкетами (в формате UTF-8)"
    )
    parser.add_argument(
        "-o", "--output",
        default="result.txt",
        help="Имя выходного файла (по умолчанию: result.txt)"
    )
    args = parser.parse_args()

    try:
        with open(args.input_file, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        print(f"Файл {args.input_file} не найден.")
        return

    # Предобработка
    content = re.sub(r'^\s*\d+\)\s*', '', content, flags=re.MULTILINE)
    content = re.sub(r'\n\s*\n', '\n\n', content)

    blocks = parse_blocks(content)
    results: List[str] = []

    for block in blocks:
        result = process_block(block)
        if result:
            results.append(result)

    # Запись результата
    with open(args.output, 'w', encoding='utf-8') as f:
        for line in results:
            f.write(line + '\n')

    # Вывод
    if results:
        for line in results:
            print(line)
    else:
        print("Нет валидных записей.")


if __name__ == "__main__":
    main()