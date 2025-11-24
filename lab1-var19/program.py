import re
import argparse
from datetime import datetime


def is_valid_email(email):
    """
    Проверяет валидность email-адреса согласно требованиям.

    Args:
        email (str): Email-адрес для проверки

    Returns:
        bool: True если email валиден, False в противном случае
    """
    # проверяем домены gmail.com, mail.ru, yandex.ru
    if not re.search(r'@(gmail\.com|mail\.ru|yandex\.ru)$', email):
        return False

    # разделяем email на локальную часть и домен
    local_part = email.split('@')[0]

    # проверяем локальную часть: буквы, цифры и символы
    if not re.match(r'^[A-Za-z0-9._%+-]+$', local_part):
        return False

    # проверяем длину локальной части (до 64 символов)
    if len(local_part) > 64 or len(local_part) == 0:
        return False

    return True


def parse_person_blocks(text):
    """
    Разбивает текст на блоки с информацией о людях.

    Args:
        text (str): Исходный текст с анкетами

    Returns:
        list: Список блоков с информацией о каждом человеке
    """
    # разделяем по номерам с закрывающей скобкой
    blocks = re.split(r'\n\d+\)\n', text)
    # первый элемент может быть пустым, если текст начинается с "1)"
    return [block.strip() for block in blocks if block.strip()]


def extract_email(block):
    """
    Извлекает email из блока с информацией о человеке.

    Args:
        block (str): Блок текста с информацией о человеке

    Returns:
        str or None: Email-адрес или None если не найден
    """
    email_match = re.search(r'Номер телефона или email:\s*(.+)', block)
    if email_match:
        return email_match.group(1).strip()
    return None


def is_email_field(value):
    """
    Проверяет, является ли значение email-адресом (а не телефоном).

    Args:
        value (str): Значение для проверки

    Returns:
        bool: True если значение содержит '@', False в противном случае
    """
    return '@' in value if value else False


def process_person_blocks(person_blocks):
    """
    Обрабатывает блоки с анкетами, разделяя на валидные и невалидные.

    Args:
        person_blocks (list): Список блоков с анкетами

    Returns:
        tuple: (valid_blocks, invalid_email_blocks) - кортеж с валидными и невалидными анкетами
    """
    invalid_email_blocks = []
    valid_blocks = []

    for i, block in enumerate(person_blocks, 1):
        email = extract_email(block)

        if email and is_email_field(email):
            if not is_valid_email(email):
                invalid_email_blocks.append((i, block))
            else:
                valid_blocks.append(block)
        else:
            # если это не email или email не указан, считаем валидным
            valid_blocks.append(block)

    return valid_blocks, invalid_email_blocks


def print_invalid_blocks(invalid_email_blocks):
    """
    Выводит информацию о невалидных анкетах.

    Args:
        invalid_email_blocks (list): Список кортежей (номер, блок) с невалидными анкетами
    """
    print("АНКЕТЫ С НЕКОРРЕКТНЫМИ EMAIL-АДРЕСАМИ:")
    print("=" * 50)

    for i, block in invalid_email_blocks:
        print(f"Анкета {i}:")
        print(block)
        print("-" * 50)


def write_valid_blocks_to_file(valid_blocks, output_filename):
    """
    Записывает валидные анкеты в файл.

    Args:
        valid_blocks (list): Список валидных анкет
        output_filename (str): Имя выходного файла
    """
    try:
        with open(output_filename, 'w', encoding='utf-8') as file:
            for i, block in enumerate(valid_blocks, 1):
                file.write(f"{i})\n")
                file.write(block)
                if not block.endswith('\n\n'):
                    file.write("\n\n")

        print(f"Результат сохранен в файл: {output_filename}")

    except Exception as e:
        print(f"Ошибка при записи файла: {e}")


def read_file(filename):
    """
    Читает содержимое файла.

    Args:
        filename (str): Путь к файлу

    Returns:
        str: Содержимое файла или None в случае ошибки
    """
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        print(f"Ошибка: Файл '{filename}' не найден")
        return None
    except PermissionError:
        print(f"Ошибка: Нет прав доступа к файлу '{filename}'")
        return None
    except Exception as e:
        print(f"Ошибка при чтении файла: {e}")
        return None


def main():
    """
    Основная функция программы для обработки анкет с некорректными email-адресами.
    """
    # парсинг аргументов командной строки
    parser = argparse.ArgumentParser(
        description='Обработка анкет с некорректными email-адресами. '
                    'Находит и удаляет анкеты с некорректными email-адресами.'
    )
    parser.add_argument(
        'input_filename',
        type=str,
        help='Путь к входному файлу с данными анкет'
    )
    parser.add_argument(
        '-o', '--output',
        type=str,
        default='valid_data.txt',
        help='Путь к выходному файлу с валидными анкетами (по умолчанию: valid_data.txt)'
    )
    args = parser.parse_args()

    # чтение файла
    content = read_file(args.input_filename)
    if content is None:
        return

    # разбиваем на блоки с информацией о людях
    person_blocks = parse_person_blocks(content)

    # обрабатываем анкеты
    valid_blocks, invalid_email_blocks = process_person_blocks(person_blocks)

    # выводим невалидные анкеты
    print_invalid_blocks(invalid_email_blocks)

    # выводим статистику
    print(f"\nНайдено анкет с некорректными email-адресами: {len(invalid_email_blocks)}")
    print(f"Всего анкет после удаления: {len(valid_blocks)}")

    # записываем валидные анкеты в файл
    write_valid_blocks_to_file(valid_blocks, args.output)


if __name__ == "__main__":
    main()
#С указанием выходного файла:
#python program.py data.txt -o output.txt
#python program.py data.txt --output processed_data.txt
