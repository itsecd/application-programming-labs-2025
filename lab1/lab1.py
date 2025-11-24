import argparse
import re


def parse_console() -> argparse.Namespace:
    """
    Парсер для аргументов в консоли
    """
    parser = argparse.ArgumentParser(description='Поиск анкет с корректными номерами телефонов')
    parser.add_argument("data_file", type=str, help="файл для чтения")
    parser.add_argument("result_file", type=str, help="файл для записи результатов")
    args = parser.parse_args()
    return args


def correct_numbers(text: str) -> list:
    """
    Извлекает анкеты с корректными номерами телефонов
    """
    profiles = re.split(r'\n\d+\)\s*\n', text.strip())
    pattern = r'(?:\+7|8)[\s\-]?\(?\d{3}\)?[\s\-]?\d{3}[\s\-]?\d{2}[\s\-]?\d{2}'
    
    correct_profiles = []
    for profile in profiles:
        if profile.strip() and re.search(pattern, profile):
            correct_profiles.append(profile.strip())
    
    return correct_profiles


def read_file(filename: str) -> str:
    """
    Читает содержимое файла
    """
    with open(filename, 'r', encoding='utf-8') as file:
        return file.read()


def write_file(filename: str, profiles: list) -> None: 
    """
    Записывает найденные анкеты в новый файл
    """
    with open(filename, 'w', encoding='utf-8') as file:
        file.write("АНКЕТЫ С КОРРЕКТНЫМИ НОМЕРАМИ ТЕЛЕФОНОВ\n")
        file.write("=" * 50 + "\n\n")
        
        for i, profile in enumerate(profiles, 1):
            file.write(f"{i})\n")
            file.write(profile)
            file.write("\n\n")


def count_total_profiles(text: str) -> int:
    """
    Подсчитывает общее количество анкет в файле
    """
    profiles = re.split(r'\n\d+\)\s*\n', text.strip())
    return len([p for p in profiles if p.strip()])


def main() -> None:
    try:
        args = parse_console()
        text = read_file(args.data_file)
        total_profiles = count_total_profiles(text)
        correct_profiles = correct_numbers(text)
        write_file(args.result_file, correct_profiles)
        
        print("=" * 50)
        print("РЕЗУЛЬТАТЫ ПОИСКА:")
        print(f"Всего анкет в файле: {total_profiles}")
        print(f"Анкет с корректными номерами: {len(correct_profiles)}")
        print(f"Результаты сохранены в файл: {args.result_file}")
        print("=" * 50)

    except FileNotFoundError:
        print("файл не найден")
    except Exception as e:
        print(f"Ошибка при чтении файла")


if __name__ == "__main__":
    main()