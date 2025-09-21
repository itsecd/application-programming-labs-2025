#Найдите анкеты людей, у которых указан номер телефона (в корректном формате).
#Выведите их количество на экран и сохраните найденные анкеты в новый файл.
import re
import argparse

def correct_number(text):
	start_string = r"[а-яА-Я\sa-zA-Z]+: "
	pattern1 = start_string + r"(\+7|8)\d{10}"
	pattern2 = start_string + r"(\+7|8)( \(\d{3}\) )\d{3}[ -]{1}\d{2}[ -]\d{2}"
	pattern3 = start_string + r"(\+7|8)( \d{3} )\d{3}[ -]{1}\d{2}[ -]\d{2}"
	return re.match(pattern1, text) or re.match(pattern2, text) or re.match(pattern3, text)


parser = argparse.ArgumentParser()
parser.add_argument("--read_file", "-rf", type=str, help = "file read name")
parser.add_argument("--write_file", "-wf", type=str, help = "file write name")
args = parser.parse_args()

count_correct_numbers = 0
if args.read_file is not None:
	with open(args.read_file, "r", encoding="utf-8") as rfile:
		text = rfile.read()
	text = text.splitlines()

	for i in range(len(text)):
		if(correct_number(text[i])):
			count_correct_numbers+=1

	print(count_correct_number)