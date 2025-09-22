import argparse
from datetime import datetime
import re
import sys


def read_file(file_path: str) -> list[str]:
    """Читает файл и делит на анкеты по пустой строке. Убирает старую нумерацию."""
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            text = file.read().strip()
    except Exception as e:
        print(f"Ошибка при чтении файла '{file_path}': {e}")
        sys.exit(1)

    # убираем строки с нумерацией вида "1)", "23)" и т.п.
    text = re.sub(r"^\d+\)\s*$", "", text, flags=re.MULTILINE)
    return text.split("\n\n")


def save_file(file_path: str, data: list[str]) -> None:
    """Сохраняет анкеты в файл с нумерацией (1), 2), 3)...)."""
    try:
        with open(file_path, "w", encoding="utf-8") as file:
            for i, profile in enumerate(data, start=1):
                file.write(f"{i})\n{profile.strip()}\n\n")
    except Exception as e:
        print(f"Ошибка при записи файла '{file_path}': {e}")
        sys.exit(1)


def profile_to_dict(profile: str) -> dict:
    """Парсит анкету в словарь {ключ: значение}."""
    result = {}
    try:
        for line in profile.splitlines():
            if ":" in line:
                key, value = line.split(":", 1)
                result[key.strip()] = value.strip()
    except Exception as e:
        print(f"Ошибка при обработке анкеты:\n{profile}\nПричина: {e}")
    return result



def is_male_profile(fields: dict) -> bool:
    """Проверяет, мужская ли анкета (строго)."""
    sex = fields.get("Пол", "").strip().lower()
    return sex in ("м", "мужской")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Фильтрация анкет: выбрать мужчин из списка"
    )
    parser.add_argument("input", help="Путь к входному файлу (например, data.txt)")
    parser.add_argument("output", help="Путь к выходному файлу (например, men_profiles.txt)")
    args = parser.parse_args()

    profiles = read_file(args.input)

    male_profiles: list[str] = []
    for profile in profiles:
        profile = profile.strip()
        if not profile:
            continue
        fields = profile_to_dict(profile)
        if not fields:
            continue
        if "Пол" not in fields or "Фамилия" not in fields or "Имя" not in fields or "Дата рождения" not in fields\
            or "Номер телефона или email" not in fields or "Город" not in fields:
            continue
        if not is_male_profile(fields):
            continue
        male_profiles.append(profile)

    print(f"Количество анкет мужчин: {len(male_profiles)}")
    save_file(args.output, male_profiles)


if __name__ == "__main__":
    main()
