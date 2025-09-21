#Найдите анкеты людей, у которых указан номер телефона (в корректном формате).
#Выведите их количество на экран и сохраните найденные анкеты в новый файл.
import re

def count_correct_numbers(text):
	pattern = r"(8|\+7)+[ (]*\d{3}[ )]*\d{3}[ -]*\d{2}[ -]*\d{2}"
	count = len(re.findall(pattern, text))
	return count




with open("data.txt", "r") as file:
	text = file.read()
print(text)

print(count_correct_numbers(text))
