import re
import argparse

with open("data.txt", "r", encoding="utf-8") as file :
    text = file.read()

pattern = "[A-Za-z0-9._%+-]+@[gmail.com|mail.ru|yandex.ru]+"
emails = re.findall(pattern, text)
print(emails)
print(len(emails))

valid_forms = []

forms = text.split("\n\n")
for form in forms :
    if re.search(pattern,form):
        valid_forms.append(form)
with open("valid_forms.txt", "w", encoding="utf8") as output :
    for form in valid_forms:
        output.write(form + "\n\n")

