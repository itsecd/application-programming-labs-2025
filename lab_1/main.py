#Найдите анкеты людей, у которых указан номер телефона (в корректном формате).
#Выведите их количество на экран и сохраните найденные анкеты в новый файл.
import re

def correct_number(text):
	start_string = r"[а-яА-Я\sa-z]+: "
	pattern1 = start_string + r"(\+7|8)\d{10}"
	pattern2 = start_string + r"(\+7|8)( \(\d{3}\) )\d{3}[ -]{1}\d{2}[ -]\d{2}"
	pattern3 = start_string + r"(\+7|8)( \d{3} )\d{3}[ -]{1}\d{2}[ -]\d{2}"
	return re.match(pattern1, text) or re.match(pattern2, text) or re.match(pattern3, text)


count_correct_number = 0

with open("data.txt", "r", encoding="utf-8") as file:
	text = file.read()
text = text.splitlines()

for line in text:
	if (correct_number(line)):
		count_correct_number+=1
print(count_correct_number)