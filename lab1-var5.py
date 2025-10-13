import re
import argparse

def main():
    # Чтение аргументов командной строки
    parser = argparse.ArgumentParser(description="Лабораторная работа № 1, вариант 5.")
    parser.add_argument("input", help="Путь к файлу с анкетами.")
    parser.add_argument("-o", "--output", default="ivanovs_forms.txt",
                        help="Имя выходного файла (по умолчанию: ivanovs_forms.txt)")

    # Сохранение введенных аргументов пользователем
    args = parser.parse_args()
    filename = args.input
    out_name = args.output

    # Открытие и чтение входного файла
    try:
        with open(filename, "r", encoding = "utf-8") as f:
            lines=f.read().splitlines()
    except FileNotFoundError:
        print("Файл не найден:", filename)
        return

    # Создание переменных для анкеты
    surname = name = gender = birthday = contact = city = None
    all_forms = []

    # Функция по добавлению анкет именно в 6 строк (т.е. полная)
    def add_if_full():
        if all([surname, name, gender, birthday, contact, city]):
            all_forms.append([f"Фамилия: {surname}",
                              f"Имя: {name}",
                              f"Пол: {gender}",
                              f"Дата рождения: {birthday}",
                              f"Номер телефона или email: {contact}",
                              f"Город: {city}"])

    # Обработка файла по строкам
    for raw in lines:
        s = raw.strip()
        if not s:
            continue
        if s.endswith(")") and s[:-1].isdigit():
            add_if_full()
            surname = name = gender = birthday = contact = city = None
            continue

        # Создание копии строки в нижнем регистре
        low = s.lower()

        # Выявление новой анкеты по началу с "фамилия"
        if low.startswith("фамилия"):
            add_if_full()
            surname = name = gender = birthday = contact = city = None
            surname = s.split(":", 1)[1].strip() if ":" in s else s
            continue

        # Проверка строк по их началу и сохранение нужных полей анкет
        elif low.startswith("имя"):
            name = s.split(":", 1)[1].strip() if ":" in s else s
        elif low.startswith("пол"):
            gender = s.split(":", 1)[1].strip() if ":" in s else s
        elif low.startswith("дата рождения"):
            birthday = s.split(":", 1)[1].strip() if ":" in s else s
        elif (low.startswith("номер телефона")
              or low.startswith("телефон")
              or low.startswith("e-mail")
              or low.startswith("email")):
            contact = s.split(":", 1)[1].strip() if ":" in s else s
        elif low.startswith("город"):
            city = s.split(":", 1)[1].strip() if ":" in s else s

    # Проверка последней анкеты
    add_if_full()

    # Фильтрация анкет по фамилии Иванов(а)
    ivanovs = []
    for form in all_forms:
        surname_value = form[0].split(":", 1)[1].strip()
        if re.fullmatch(r"(?i)иванов(а)?", surname_value):
            ivanovs.append(form)

    # Сохранение найденных анкет в файл
    with open(out_name, "w", encoding="utf-8-sig") as out:
        for form in ivanovs:
            out.write("\n".join(form) + "\n\n")

    # Вывод информации в консоль
    print("Найдено анкет:", len(ivanovs))
    print("Результаты сохранены в", out_name)

if __name__ == "__main__":
    main()