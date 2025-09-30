import re
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("input", type=str, help="input file path")
args = parser.parse_args()

with open(args.input, "r", encoding="utf-8") as file :
    text = file.read()

pattern = r"[A-Za-z0-9._%+-]+@(?:gmail\.com|mail\.ru|yandex\.ru)"
valid_forms = []

forms = text.split("\n\n")
for form in forms :
    if re.search(pattern,form):
        valid_forms.append(form)
with open("valid_forms.txt", "w", encoding="utf8") as output :
    for form in valid_forms:
        output.write(form + "\n\n")
print(f"Количество анкет с верно указанными почтами: {len(valid_forms)}")
print("Данные анкеты сохранены в файл valid_forms.txt")

