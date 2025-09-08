import argparse
import re


def parse_args():
    #Парсинг аргументов командной строки
    parser = argparse.ArgumentParser()
    parser.add_argument('path', type=str, help='Path to file (Путь к файлу)')
    return parser.parse_args()


def read_file(path):
    #Чтение файла
    with open(path, "r", encoding="utf-8") as file:
        return file.read()


def split_forms(data):
    #Разделение на формы имя, фамилия и тп
    return data.split("\n\n")


def filter_forms_by_email(forms):
    #разделение по почтам
    email_pattern = r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}'
    with_email = [form for form in forms if re.search(email_pattern, form)]
    without_email = [form for form in forms if not re.search(email_pattern, form)]
    return with_email, without_email


def save_forms_to_file(forms, filename):
    #сохранение в файл
    with open(filename, "w", encoding="utf-8") as file:
        file.write("\n\n".join(forms))


def main():
    args = parse_args()
    data = read_file(args.path)
    forms = split_forms(data)
    form_with_mail, form_without_mail = filter_forms_by_email(forms)

    print("Без почты:")
    for trash in form_without_mail:
        print("\n" + trash)

    save_forms_to_file(form_with_mail, "good_file.txt")


if __name__ == "__main__":
    main()