import re
import argparse

# Кокшина Анна Александровна 6211-100503

def is_validate(person: list[str, str, str, str, str, str]) -> bool:
    """Провереряет корректность данных анкеты"""
    if not person[0][0].isupper():
        return False

    if not person[1][0].isupper():
        return False

    if person[2] not in ["М", "м", "Мужской", "мужской", "Ж", "ж", "Женский", "женский"]:
        return False

    if not re.fullmatch(r"\d{1,2}[./-]\d{1,2}[./-]\d{4}", person[3]):
        return False
    day, month, year = map(int, re.split(r"[./-]", person[3]))
    if not (1900 <= year <= 2025 and 1 <= month <= 12 and 1 <= day <= 31):
        return False
    if day == 31 and month in [2, 4, 6, 9, 11]:
        return False
    if (month == 2 and day > 28) or\
            (month == 2 and day > 29 and (year % 4 == 0 or year % 400 == 0) and year % 100 != 0):
            return False

    if not (re.fullmatch(r"[+]7\d{10}", person[4]) or re.fullmatch(r"8\d{10}", person[4]) or \
        re.fullmatch(r"8\s[(]?\d{3}[)]?\s\d{3}[\s-]\d{2}[\s-]\d{2}", person[4]) or \
        re.fullmatch(r"[+]7\s[(]?\d{3}[)]?\s\d{3}[\s-]\d{2}[\s-]\d{2}", person[4])):

        if person[4][person[4].find("@")+1:] not in ["gmail.com", "mail.ru", "yandex.ru"]:
            return False
        if not re.fullmatch(r"[A-Za-z0-9._%+-]{,64}",person[4][:person[4].find("@")]):
            return False
    return True


def main():
    parser = argparse.ArgumentParser()  # создание экземпляра парсера
    parser.add_argument('file_name', type=str, help='Укажите путь к файлу')  # добавление позиционного аргумента командной строки
    args = parser.parse_args()  # парсинг аргументов
    if args.file_name == None:
        print("Укажите путь")
    else:
        try:
            file = open(args.file_name, "r", encoding="utf-8")
            data = file.readlines()
            file.close()
        except:
            print("Ошибка открытия файла")
            exit(1)
        person = []
        names = {}
        for line in data:
            if re.fullmatch(r"\d+[)]\n", line) or line == "\n":
                person.clear()
                continue
            person.append(line[line.find(":")+2:-1])
            if len(person) == 6:
                if not is_validate(person):
                    continue
                if person[1] not in names:
                    names[person[1]] = 1
                else:
                    names[person[1]] += 1

        max_count = 0
        max_name = ""
        for name, count in names.items():
            if max_count < count:
                max_count = count
                max_name = name
        print(f"Самое частое имя {max_name} и количество повторений: {max_count}")


if __name__ == "__main__":
    main()

