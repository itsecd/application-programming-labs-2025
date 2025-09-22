import sys
import re


def read_file(file_path: str) -> list[str]:
    """Читает файл и делит на анкеты по пустой строке. Убирает старую нумерацию."""
    with open(file_path, "r", encoding="utf-8") as file:
        text = file.read().strip()
    text = re.sub(r"^\d+\)\s*$", "", text, flags=re.MULTILINE)
    return text.split("\n\n")


def save_file(file_path: str, data: list[str]) -> None:
    """Сохраняет анкеты в файл с нумерацией (1), 2), 3)...)."""
    with open(file_path, "w", encoding="utf-8") as file:
        for i, profile in enumerate(data, start=1):
            file.write(f"{i})\n{profile.strip()}\n\n")


def profile_to_dict(profile: str) -> dict:
    """Парсит анкету в словарь {ключ: значение}."""
    result = {}
    for line in profile.splitlines():
        if ":" in line:
            key, value = line.split(":", 1)
            result[key.strip()] = value.strip()
    return result



def is_male_profile(fields: dict) -> bool:
    """Проверяет, мужская ли анкета."""
    sex = fields.get("Пол", "").strip().lower()
    return sex.startswith("м")  # М, м, Мужской, мужской


def main() -> None:
    if len(sys.argv) < 2:
        print("Ошибка: укажите путь к файлу с анкетами.")
        print("Пример: python lab.py data.txt")
        sys.exit(1)

    file_path = sys.argv[1]

    try:
        profiles = read_file(file_path)
    except FileNotFoundError:
        print(f"Ошибка: файл '{file_path}' не найден.")
        sys.exit(1)

    male_profiles: list[str] = []
    for profile in profiles:
        profile = profile.strip()
        if not profile:
            continue
        fields = profile_to_dict(profile)
        if fields and is_male_profile(fields):
            male_profiles.append(profile)

    print(f"Количество анкет мужчин: {len(male_profiles)}")

    save_file("men_profiles.txt", male_profiles)


if __name__ == "__main__":
    main()
