import csv
from icrawler.builtin import GoogleImageCrawler
import requests

def get_keyword() -> str:
	"""
	Получение от пользователя ключевых слов
	"""
	keyword = input("Введите ключевое слово: ")
	return keyword

def main() -> None:
	try:
		keyword1 = "dog" # заменить потом
		keyword2 = "cat" # заменить потом
		print(keyword1, keyword2)
	except Exception as exc:
		print(f"Возникла ошибка: {exc}")

if __name__ == "__main__":
	main()