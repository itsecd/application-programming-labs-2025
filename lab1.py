import argparse
import re


def read_file(filename: str) -> str:
    """
    Читает содержимое файла и возвращает его в виде строки.
    """
    try:
        with open(filename, "r", encoding="utf-8") as file:
            return file.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"Файл '{filename}' не найден!")


def struct_ancet_from_file(text: str) -> list[str]:
    """
    Разделяет текст на отдельные анкеты по пустым строкам.
    """
    forms = text.strip().split("\n\n")
    return forms


def parse_arguments() -> str:
    """
    Парсит аргументы командной строки.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("fname", type=str, help="Имя входного файла")
    args = parser.parse_args()
    return args.fname


def parse_form(form: str) -> dict:
    """
    Разбор одной анкеты. Выбрасывает ValueError, если нет имени или пола.
    """
    lastname_match = re.search(r"Фамилия:\s*(.+)", form)
    firstname_match = re.search(r"Имя:\s*(.+)", form)
    sex_match = re.search(r"Пол:\s*(.+)", form)
    birthday_match = re.search(r"Дата рождения:\s*(.+)", form)
    phone_match = re.search(r"Номер телефона или email:\s*(.+)", form)
    city_match = re.search(r"Город:\s*(.+)", form)

    if not firstname_match or not sex_match:
        raise ValueError("Анкета неполная: отсутствует Имя или Пол")
    
    return {
        "lastname": lastname_match.group(1).strip() if lastname_match else "",
        "firstname": firstname_match.group(1).strip(),
        "sex": sex_match.group(1).strip(),
        "birthday": birthday_match.group(1).strip() if birthday_match else "",
        "phone": phone_match.group(1).strip() if phone_match else "",
        "city": city_match.group(1).strip() if city_match else "",
    }


def filter_forms(forms: list[str]) -> tuple[list[dict], int]:
    """
    Фильтрует анкеты по критерию: женский пол и имя на "А".
    """
    filtered_forms = []
    count = 0

    for form in forms:
        try:
            data = parse_form(form)
        except ValueError as exc:
            print(f"Пропускаем анкету: {exc}")
            continue

        if (
            data["sex"].lower() in ["ж", "женский"]
            and data["firstname"][0].lower() == "а"
        ):
            count += 1
            filtered_forms.append(data)

    return filtered_forms, count


def write_results(filtered_forms: list[dict], output_filename: str = "newdata.txt") -> None:
    """
    Записывает отфильтрованные анкеты в выходной файл.
    """
    with open(output_filename, "w", encoding="utf-8") as f_out:
        for data in filtered_forms:
            f_out.write(
                f"Фамилия: {data['lastname']}\n"
                f"Имя: {data['firstname']}\n"
                f"Пол: {data['sex']}\n"
                f"Дата рождения: {data['birthday']}\n"
                f"Номер телефона или email: {data['phone']}\n"
                f"Город: {data['city']}\n\n"
            )


def main() -> None:
    """
    Основная функция программы.
    """
    filename = parse_arguments()

    try:
        text = read_file(filename)
        forms = struct_ancet_from_file(text)

        filtered_forms, count = filter_forms(forms)
        write_results(filtered_forms)

        print(f"Количество женщин с именем на 'А': {count}")
        print("Файл 'newdata.txt' успешно создан.")
    except Exception as exc:
        print(f"Error: {exc}")


if __name__ == "__main__":
    main()