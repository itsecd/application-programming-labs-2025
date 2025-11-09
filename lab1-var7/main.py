import argparse
import re


def is_valid_phone(phone: str) -> bool:
    '''
    проверка валидности номера телефона с кодом 927
    '''
    pattern = r'^(?:\+7|8)\s*\(?927\)?[\s-]?\d{3}[\s-]?\d{2}[\s-]?\d{2}$'
    match = re.search(pattern, phone)
    return bool(match)


def extract_records_with_927(text: str) -> list[str]:

    #разделение анкет и выбор тех, где телефон имеет код 927

    records = re.split(r'\n\d+\)\n|\n\s*\n', text.strip())
    valid_records = []

    for record in records:
        for line in record.split('\n'):
            if re.match(r'\s*Номер телефона или email:', line):
                contact = line.split(':', 1)[1].strip()

                contact_cleaned = re.sub(r'\s+', ' ', contact)
                if is_valid_phone(contact_cleaned):
                    valid_records.append(record.strip())
                    break

    return valid_records


def read_file(file_name: str) -> str:

    #чтение данных из файла

    with open(file_name, "r", encoding="utf-8") as file:
        return file.read()


def write_file(records: list[str]) -> None:

    #запись найденных анкет в файл result.txt

    with open("result.txt", "w", encoding="utf-8") as file:
        for record in records:
            file.write(record + "\n\n")

    print(f"Результаты сохранены в файл: result.txt")


def main():
    parser = argparse.ArgumentParser(description="Поиск анкет с телефоном, имеющим код города 927")
    parser.add_argument("file_name", type=str, help="Имя входного файла (например, data.txt)")
    args = parser.parse_args()
    try:
        text = read_file(args.file_name)
        records = extract_records_with_927(text)
        print(f"Найдено анкет с кодом города 927: {len(records)}")

        if records:
            write_file(records)
        else:
            print("Подходящих анкет не найдено.")
    except FileNotFoundError:
        print("Ошибка: файл не найден.")


if __name__ == "__main__":
    main()
