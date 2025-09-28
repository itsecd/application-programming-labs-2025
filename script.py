import re
import sys
from typing import List


def read_file(file_path: str) -> str:
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()


def write_file(file_path: str, data: List[str]) -> None:
    with open(file_path, "w", encoding="utf-8") as f:
        f.write("\n\n".join(data))


def extract_ankets_with_invalid_email(content: str) -> List[str]:
    ALLOWED_DOMAINS = [
        'gmail.com',
        'mail.ru',
        'yandex.ru'
    ]
    valid_email_pattern = re.compile(
        r"\b[A-Za-z0-9._%+-]{1,64}"
        r"@(gmail\.com|mail\.ru|yandex\.ru)\b"
    )

    ankets = re.split(r"\n\s*\n", content.strip())

    invalid_anktes = []
    for anket in ankets:
        for line in anket.split('\n'):
            if 'Номер телефона или email:' in line:
                email_phone_line = line
                if '@' in email_phone_line:
                    valid_email_match = valid_email_pattern.search(
                        email_phone_line)
                    if not valid_email_match:
                        if re.search(r'[А-Яа-я]', email_phone_line):
                            invalid_anktes.append(anket)
                            break
                        elif any(
                                domain in email_phone_line
                                for domain in ALLOWED_DOMAINS):
                            invalid_anktes.append(anket)
                            break
                elif any(
                        domain in email_phone_line
                        for domain in ALLOWED_DOMAINS):
                    if not re.search(r'\+\d|\(\d| \d{3}', email_phone_line):
                        invalid_anktes.append(anket)
                        break
                break
    return invalid_anktes


def remove_ankets_with_invalid_email(
    content: str,
        invalid_ankets: List[str]
) -> List[str]:
    ankets = re.split(r"\n\s*\n", content.strip())
    invalid_set = set(invalid_ankets)
    return [anket for anket in ankets if anket not in invalid_set]


def main() -> None:
    if len(sys.argv) < 2:
        print("Использование: python script.py <входной-файл> <выходной-файл>")
        return

    input_file = sys.argv[1]
    output_file = sys.argv[2]
    content = read_file(input_file)
    invalid_ankets = extract_ankets_with_invalid_email(content)

    print("Анкеты с некорректным email:")
    print("=" * 80)
    for i, anket in enumerate(invalid_ankets, 1):
        print(anket)
        print("=" * 80)

    print(f"\nВсего найдено {len(invalid_ankets)} анкет с некорректным email.")
    cleaned_ankets = remove_ankets_with_invalid_email(content, invalid_ankets)
    write_file(output_file, cleaned_ankets)
    print(f"\nУдалено {len(invalid_ankets)} анкет с некорректным  email.")
    print(f"Сохранено {len(cleaned_ankets)} анкет в файл: {output_file}")


if __name__ == "__main__":
    main()
