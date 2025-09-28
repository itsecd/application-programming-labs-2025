import re
import sys
from typing import List


def read_file(file_path: str) -> str:
    """
    Функция для чтения содержимого файла.

    Args:
        file_path (str): Путь к файлу для чтения

    Returns:
        str: Содержимое файла в виде строки

    Raises:
        FileNotFoundError: Если файл не найден
        PermissionError: Если нет прав для чтения файла
        UnicodeDecodeError: Если ошибка кодировки файла
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"Файл '{file_path}' не найден")
    except PermissionError:
        raise PermissionError(f"Нет прав для чтения файла '{file_path}'")
    except UnboundLocalError:
        raise UnicodeDecodeError(
            "Ошибка кодировки файла."
        )


def write_file(file_path: str, data: List[str]) -> None:
    """
    Записывает список анкет в файл.

    Args:
        file_path (str): Путь к входному файлу
        data (List[str]): Список анкет для записи

    Raises:
        PermissionError: Если нет прав для записи в файл
        IOError: Если произошла ошибка ввода-вывода
    """
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write("\n\n".join(data))
    except PermissionError:
        raise PermissionError(f"Нет прав для записи в файл '{file_path}'")
    except IOError as e:
        raise IOError(f"Ошибка записи в файл '{file_path}': {e}")


def extract_ankets_with_invalid_email(content: str) -> List[str]:
    """
    Функция для извлечения анкет с некорректным email.

    Args:
        content (str): Содержимое файла с анкетами

    Returns:
        List[str]: список анкет с некорректными email

    Raises:
        ValueError: если содержимое файла имеет некорректный формат
    """
    if not content or not content.strip():
        raise ValueError("Файл пуст")

    ALLOWED_DOMAINS = [
        'gmail.com',
        'mail.ru',
        'yandex.ru'
    ]

    valid_email_pattern = re.compile(
        r"\b[A-Za-z0-9._%+-]{1,64}"
        r"@(gmail\.com|mail\.ru|yandex\.ru)\b"
    )

    try:
        ankets = re.split(r"\n\s*\n", content.strip())
    except re.error as e:
        raise ValueError(f"Ошибка при чтении анкет: {e}")

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
    """
    Функция для удаления анкет с некорректным email

    Args:
        content (str): Содержимое файла с анкетами
        invalid_ankets (List[str]): Список анкет для удаления

    Returns:
        List[str]: Список анкет без некорректных email

    Raises:
        ValueError: Если содержимое файла имеет некорректный формат
    """
    if not content or not content.strip():
        raise ValueError("Файл пуст")

    try:
        ankets = re.split(r"\n\s*\n", content.strip())
    except re.error as e:
        raise ValueError(f"Ошибка при чтении анкет: {e}")

    invalid_set = set(invalid_ankets)
    return [anket for anket in ankets if anket not in invalid_set]


def main() -> None:
    """
    Основная функция программы.

    Обрабатывает аргументы CLI, находит и удаляет анкеты с некорректыми email
    """
    try:
        if len(sys.argv) < 3:
            print("Использование:"
                  " python script.py <входной-файл> <выходной-файл>")
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

        print(
            f"\nНайдено {len(invalid_ankets)} анкет с некорректным email.")
        cleaned_ankets = remove_ankets_with_invalid_email(
            content, invalid_ankets)
        write_file(output_file, cleaned_ankets)
        print(f"\nУдалено {len(invalid_ankets)} анкет с некорректным  email.")
        print(f"Сохранено {len(cleaned_ankets)} анкет в файл: {output_file}")
    except FileNotFoundError as e:
        print(f"Ошибка {e}")
        sys.exit(1)
    except PermissionError as e:
        print(f"Ошибка прав доступа {e}")
        sys.exit(1)
    except ValueError as e:
        print(f"Ошибка данных: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Неизвестная ошибка: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
