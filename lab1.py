import re
import argparse
from datetime import datetime
from typing import List


def parse_arguments() -> argparse.Namespace:
    """
    Парсинг аргументов командной строки.

    """
    parser = argparse.ArgumentParser(description='Поиск людей возрастом 30-40 лет')
    parser.add_argument('input_file', type=str, help='Путь к входному файлу с данными')
    parser.add_argument('-o', '--output', type=str, help='Путь к выходному файлу',
                        default='profiles_30_40.txt')
    return parser.parse_args()


def read_profiles(filename: str) -> List[str]:
    """
    Чтение и разделение данных на анкеты.

    """
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            content = file.read()
        return content.split('\n\n')
    except FileNotFoundError:
        raise FileNotFoundError(f"Ошибка: файл {filename} не найден")
    except Exception as e:
        raise Exception(f"Ошибка при чтении файла: {e}")


def extract_age_from_profile(profile: str, current_year: int) -> int:
    """
    Извлечение возраста из анкеты.

    """
    date_match = re.search(r'(\d{1,2})[/.-](\d{1,2})[/.-](\d{4})', profile)

    if date_match:
        try:
            day = int(date_match.group(1))
            month = int(date_match.group(2))
            year = int(date_match.group(3))

            if 1900 <= year <= current_year and 1 <= month <= 12 and 1 <= day <= 31:
                return current_year - year
        except ValueError:
            return -1
    return -1


def find_profiles_by_age(profiles: List[str], min_age: int, max_age: int) -> List[str]:
    """
    Поиск анкет по возрастному диапазону.

    """
    current_year = datetime.now().year
    matching_profiles = []

    for profile in profiles:
        age = extract_age_from_profile(profile, current_year)
        if min_age <= age <= max_age:
            matching_profiles.append(profile)

    return matching_profiles


def save_profiles(profiles: List[str], filename: str) -> None:
    """
    Сохранение анкет в файл.

    """
    try:
        with open(filename, 'w', encoding='utf-8') as output_file:
            for profile in profiles:
                output_file.write(profile + '\n\n')
    except Exception as e:
        raise Exception(f"Ошибка при сохранении файла: {e}")


def main() -> None:
    """
    Основная функция программы.
    """
    try:
        args = parse_arguments()
        profiles = read_profiles(args.input_file)

        matching_profiles = find_profiles_by_age(profiles, 30, 40)

        print(f"Количество людей возрастом от 30 до 40 лет: {len(matching_profiles)}")

        save_profiles(matching_profiles, args.output)
        print(f"Анкеты сохранены в файл '{args.output}'")

    except Exception as e:
        print(f"Ошибка: {e}")


if __name__ == "__main__":
    main()