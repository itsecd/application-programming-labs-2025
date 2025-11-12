import argparse
import re


def parse_args() -> tuple[str, str]:
    """
    Чтение аргументов командной строки
    """
    parser = argparse.ArgumentParser(description="Лабораторная работа № 1, вариант 5.")
    parser.add_argument("input", help="Путь к файлу с анкетами.")
    parser.add_argument("-o", "--output", default="ivanovs_forms.txt",
                        help="Имя выходного файла (по умолчанию: ivanovs_forms.txt)")
    args = parser.parse_args()
    return args.input, args.output


def read_lines(filename: str) -> list[str]:
    """
    Открытие и чтение входного файла
    """
    try:
        with open(filename, "r", encoding = "utf-8") as f:
            return f.read().splitlines()
    except FileNotFoundError:
        raise FileNotFoundError("Файл не найден:", filename)


def add_if_full(lines: list[str]) -> list[list[str]]:
    """
    Функция по добавлению анкет именно в 6 строк
    """
    # Создание переменных для анкеты
    surname = name = gender = birthday = contact = city = None
    all_forms: list[list[str]] = []

    # Обработка файла по строкам
    for raw in lines:
        s = raw.strip()
        if not s:
            continue
        if s.endswith(")") and s[:-1].isdigit():
            if all([surname, name, gender, birthday, contact, city]):
                all_forms.append([f"Фамилия: {surname}",
                                  f"Имя: {name}",
                                  f"Пол: {gender}",
                                  f"Дата рождения: {birthday}",
                                  f"Номер телефона или email: {contact}",
                                  f"Город: {city}"])
            surname = name = gender = birthday = contact = city = None
            continue
        # Создание копии строки в нижнем регистре
        low = s.lower()

        # Проверка строк по их началу и сохранение нужных полей анкет
        if low.startswith("фамилия"):
            surname = s.split(":", 1)[1].strip() if ":" in s else s
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
    if all([surname, name, gender, birthday, contact, city]):
        all_forms.append([f"Фамилия: {surname}",
                          f"Имя: {name}",
                          f"Пол: {gender}",
                          f"Дата рождения: {birthday}",
                          f"Номер телефона или email: {contact}",
                          f"Город: {city}"])
    return all_forms


def filter_ivanovs(forms: list[list[str]]) -> list[list[str]]:
    """
    Фильтрация анкет по фамилии Иванов(а)
    """
    ivanovs: list[list[str]] = []
    for form in forms:
        surname_value = form[0].split(":", 1)[1].strip()
        if re.fullmatch(r"(?i)иванов(а)?", surname_value):
            ivanovs.append(form)
    return ivanovs


def write_forms(forms: list[list[str]], filename: str) -> None:
    """
    Запись анкет в текстовый файл
    """
    with open(filename, "w", encoding="utf-8") as out:
        for form in forms:
            out.write("\n".join(form) + "\n\n")


def main() -> None:
    """
    Главная функция
    """
    args_input, args_output = parse_args()

    try:
        lines = read_lines(args_input)
        # Обработка анкет из файла
        all_forms = add_if_full(lines)

        # Поиск и сохранение анкет с "Иванов(а)"
        ivanovs = filter_ivanovs(all_forms)

        # Запись результата
        write_forms(ivanovs, args_output)

        # Вывод
        print("Найдено анкет:", len(ivanovs))
        print("Результаты сохранены в", args_output)
    except Exception as ex:
        print("Ошибка: ", ex)


if __name__ == "__main__":
    main()