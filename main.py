import argparse
import re


def is_valid_email(email: str) -> bool:
    """ 
    Проверка валидности email.
    """
    pattern = r'^[A-Za-z0-9._%+-]{1,64}@(gmail\.com|mail\.ru|yandex\.ru)$'
    match = re.search(pattern, email)

    return bool(match)


def surname_and_email(record: str) -> tuple[str | None, str | None]:
    """ 
    Извлечение фамилии и валидного email. 
    """
    dataset = record.split('\n')
    surname = None
    email = None

    for data in dataset:
        if re.match(r'\s*Фамилия:', data):
            surname = data.split(r': ', 1)[1]

        elif re.match(r'\s*Номер телефона или email:', data):
            unfiltered_email = data.split(r': ', 1)[1]
            if is_valid_email(unfiltered_email):
                email = unfiltered_email

    return surname, email


def add_surname_email_pairs(text: str) -> list[str]:
    """ 
    Запись подходящих фамилий-email в результат.
    """
    records = re.split(r'\n\d+\)\n', text)
    result = []

    for record in records:
        surname, email = surname_and_email(record)
        if surname and email:
            result.append(f'{surname}: {email}')
    
    return result


def read_file(file_name: str) -> str:
    """ 
    Чтение из файла.
    """
    with open(file_name, "r", encoding="utf-8") as file:
        text = file.read()

    return text
    

def write_file(text: str) -> None:
    """ 
    Запись в файл.
    """
    with open("result.txt", "w", encoding="utf-8") as file:
        for person in add_surname_email_pairs(text):
            file.write(person + '\n')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('file_name', type=str)
    args = parser.parse_args()
    print(f"The name of the file is: {args.file_name}")

    try:
        write_file(read_file(args.file_name))
    except FileNotFoundError:
        print("Ошибка: файл не найден")


if __name__ == "__main__":
    main()