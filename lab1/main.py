import argparse
from functions import read_file, parse_profiles, find_oldest_and_youngest, format_profile


def main() -> None:
    parser = argparse.ArgumentParser(description="Поиск самого старого и самого молодого человека в анкетах")
    parser.add_argument("filename", type=str, help="Путь к файлу с анкетами")
    args = parser.parse_args()

    try:
        content = read_file(args.filename)
        profiles = parse_profiles(content)

        oldest, youngest = find_oldest_and_youngest(profiles)

        print("Самый старый человек:\n")
        print(format_profile(oldest))
        print("\nСамый молодой человек:\n")
        print(format_profile(youngest))

    except (FileNotFoundError, IOError, ValueError) as e:
        print(f"Ошибка: {e}")


if __name__ == "__main__":
    main()
