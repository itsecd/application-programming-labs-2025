import argparse
import re

parser = argparse.ArgumentParser()
parser.add_argument('path', type=str, help='path to file (Путь к файлу)')
args = parser.parse_args()

with open(args.path, "r", encoding="utf-8") as file:
    data = file.read()
forms = data.split("\n\n")


email_pattern = r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}'
form_without_mail = [form for form in forms if not re.search(email_pattern,form)]
form_with_mail = [form for form in forms if re.search(email_pattern,form)]

print("Без почты:")
for trash in form_without_mail:
    print("\n" + trash)

with open("good_file.txt", "w", encoding="utf-8") as file:
    file.write("\n\n".join(form_with_mail))