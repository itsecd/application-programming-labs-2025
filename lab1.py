import re
import argparse

def input_argument():
    """
    С помощью аругмента забирает путь к исходному файлу
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=str, help="input file path")
    args = parser.parse_args()
    return args

def read_file(file_path):
    """
    Считывает файл
    """
    with open(file_path, "r", encoding="utf-8") as file :
        text = file.read()
    return text

def form_with_email(text):
    """
    Отбирает анкеты с электронной почтой
    """
    pattern = r"[A-Za-z0-9._%+-]+@(?:gmail\.com|mail\.ru|yandex\.ru)"
    valid_forms = []
    forms = text.split("\n\n")
    for form in forms :
        if re.search(pattern,form):
            valid_forms.append(form)
    return valid_forms

def write_to_file(valid_forms):
    """
    Записывает подходящие анкеты в отдельный файл
    """
    with open("valid_forms.txt", "w", encoding="utf8") as output :
        for form in valid_forms:
            output.write(form + "\n\n")

def main():
    args = input_argument()
    text = read_file(args.input)
    valid_forms = form_with_email(text)
    write_to_file(valid_forms)
    print(f"Количество анкет с верно указанной почтой: {len(valid_forms)}")
    print("Отобранные анкеты сохранены в файл valid_forms.txt")

if __name__ == '__main__':
    main()


