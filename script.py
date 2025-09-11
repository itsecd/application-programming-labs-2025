import re
import sys
from typing import List


def extract_ankets_with_email(content: str) -> List[str]:
    """
    Извлекает анкеты, содержащие корректные email.

    Под корректным email понимается адрес с доменами:
    gmail.com, mail.ru, yandex.ru.

    Args:
        content (str): Содержимое файла с анкетами.

    Returns:
        List[str]: Список анкет с корректными email.
    """
    email_pattern = re.compile(
        r"\b[A-Za-z0-9._%+-]{1,64}"
        r"@(gmail\.com|mail\.ru|yandex\.ru)\b"
    )

    ankets = re.split(r"\n\s*\n", content.strip())
    return [a for a in ankets if email_pattern.search(a)]


def read_file(file_path: str) -> str:
    """
    Читает содержимое файла.

    Args:
        file_path (str): Путь к файлу.

    Returns:
        str: Содержимое файла в виде строки.
    """
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()


def write_file(file_path: str, data: List[str]) -> None:
    """
    Записывает список анкет в файл.

    Args:
        file_path (str): Путь к выходному файлу.
        data (List[str]): Список анкет для записи.
    """
    with open(file_path, "w", encoding="utf-8") as f:
        f.write("\n\n".join(data))


def main() -> None:
    """
    Основная функция программы.

    Считывает имя входного файла из аргументов командной строки,
    извлекает анкеты с корректными email и сохраняет их в файл
    emails.txt.
    """
    if len(sys.argv) < 2:
        print("Укажите имя входного файла, например: data.txt")
        return

    input_file = sys.argv[1]
    output_file = "emails.txt"

    content = read_file(input_file)
    ankets_with_email = extract_ankets_with_email(content)
    write_file(output_file, ankets_with_email)

    print(f"Найдено {len(ankets_with_email)} анкет с корректным email.")
    print(f"Результат сохранён в файл: {output_file}")


if __name__ == "__main__":
    main()
