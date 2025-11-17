import re
import argparse

def process_file(filename: str):
    """
    Чтение файла и возврат списка анкет.
    """
    try:
        with open(filename, "r", encoding="utf-8") as file:
            text = file.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"Файл '{filename}' не найден!")

    # Разделяем анкеты по пустой строке
    forms = text.strip().split('\n\n')
    return forms

def parse_form(form: str):
    """
    Порядок одной анкеты. Выбрасывает ValueError, если нет имени или пола.
    """
    lastname_match = re.search(r'Фамилия:\s*(.+)', form)
    firstname_match = re.search(r'Имя:\s*(.+)', form)
    sex_match = re.search(r'Пол:\s*(.+)', form)
    birthday_match = re.search(r'Дата рождения:\s*(.+)', form)
    phone_match = re.search(r'Номер телефона или email:\s*(.+)', form)
    city_match = re.search(r'Город:\s*(.+)', form)

    if not firstname_match or not sex_match:
        raise ValueError("Анкета неполная: отсутствует Имя или Пол")

    return {
        "lastname": lastname_match.group(1).strip() if lastname_match else "",
        "firstname": firstname_match.group(1).strip(),
        "sex": sex_match.group(1).strip(),
        "birthday": birthday_match.group(1).strip() if birthday_match else "",
        "phone": phone_match.group(1).strip() if phone_match else "",
        "city": city_match.group(1).strip() if city_match else ""
    }

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('fname', type=str, help='Имя входного файла')
    args = parser.parse_args()
    filename = args.fname

    try:
        forms = process_file(filename)
    except FileNotFoundError as exc:
        print(f"Error: {exc}")
        return

    filtered_forms = []
    count = 0

    for form in forms:
        try:
            data = parse_form(form)
        except ValueError as exc:
            print(f"Пропускаем анкету: {exc}")
            continue  # пропускаем некорректные анкеты

        # Фильтр: женский пол + имя на "А"
        if data["sex"].lower() in ['ж', 'женский'] and data["firstname"][0].lower() == 'а':
            count += 1
            filtered_forms.append(data)

    # Запись подходящих анкет в файл
    with open("newdata.txt", "w", encoding="utf-8") as f_out:
        for data in filtered_forms:
            f_out.write(
                f"Фамилия: {data['lastname']}\n"
                f"Имя: {data['firstname']}\n"
                f"Пол: {data['sex']}\n"
                f"Дата рождения: {data['birthday']}\n"
                f"Номер телефона или email: {data['phone']}\n"
                f"Город: {data['city']}\n\n"
            )

    print(f"Количество женщин с именем на 'А': {count}")
    print("Файл 'newdata.txt' успешно создан.")

if __name__ == "__main__":
    main()