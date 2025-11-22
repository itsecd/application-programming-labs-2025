import re


def format(text: str) -> str:
    if text[-1] == '\n':
        text = text[:-1]
    return text


def parse(content: list[str]) -> list:
    profiles = list()
    for i in range((len(content) + 1) // 8):
        profile = {
            "surname": format(content[i * 8 + 1][9:]),
            "name": format(content[i * 8 + 2][5:]),
            "gender": format(content[i * 8 + 3][5:]),
            "DoB": format(content[i * 8 + 4][15:]),
            "contact": format(content[i * 8 + 5][26:]),
            "city": format(content[i * 8 + 6][7:])
        }
        profiles.append(profile)
    return profiles


def print_profile(profile: dict, N: int = -1) -> None:
    if N != -1:
        print(str(N) + ")")
    print("Фамилия: " + profile["surname"])
    print("Имя: " + profile["name"])
    print("Пол: " + profile["gender"])
    print("Дата рождения: " + profile["DoB"])
    print("Номер телефона или email: " + profile["contact"])
    print("Город: " + profile["city"])


def check_phone(contact: str) -> int:
    """
    Проверяет валидность номера телефона
    0 - не валидный номер
    1 - валидный номер
    2 - почта (приравнивается к валидному номеру и игнорируется)
    """
    if contact[-1] == "u" or contact[-1] == "m":
        return 2
    pattern = r'^(\+7|8)\s?\(?\d{3}\)?\s?\d{3}(\s|\-)?\d{2}(\s|\-)?\d{2}$'
    if re.fullmatch(pattern, contact):
        return 1
    else:
        return 0


def handle(profiles: list[dict], filename: str = "profiles.txt") -> None:
    """
    Находит номера телефонов с некорректным форматом, выводит их, удаляет из profiles и записывает в filename.
    """
    cur = 0
    bad_profiles = []
    while cur < len(profiles):
        if check_phone(profiles[cur]["contact"]):
            cur += 1
        else:
            bad_profiles.append(profiles[cur])
            profiles.pop(cur)
    if not bad_profiles:
        print("Все номера корректны")
    else:
        write_to_file(bad_profiles)
        for i in range(len(bad_profiles)):
            print_profile(bad_profiles[i], i + 1)
        write_to_file(profiles, "data.txt")


def write_to_file(profiles: list[dict], name: str = "profiles.txt") -> None:
    if not len(profiles):
        raise RuntimeError("List is empty")
    with open(name, "w", encoding="utf-8") as file:
        count = 1
        for profile in profiles:
            file.writelines([
                str(count) + ")\n",
                "Фамилия: " + profile["surname"] + "\n",
                "Имя: " + profile["name"]+ "\n",
                "Пол: " + profile["gender"] + "\n",
                "Дата рождения: " + profile["DoB"] + "\n",
                "Номер телефона или email: " + profile["contact"] + "\n",
                "Город: " + profile["city"] + "\n",
                "\n"
            ])
            count += 1
            


def main():
    with open("data.txt", "r", encoding="utf-8") as file:
        content = file.readlines()
    profiles = parse(content)
    handle(profiles)

if __name__ == "__main__":
    main()