import datetime
import re
import argparse


def file_open(filename: str) -> list[str]:
    """
    принимает имя файла открывает его
    и считывает в список строк
    каждого человека в отдельную строку
    """
    result = []
    text = ""

    try:
        with open(filename, "r", encoding='utf-8') as file:
            text = file.read()
    except FileNotFoundError:
        print("Error. File not found.")
        return None
    result = re.split(r"\n\n", text)
    return result


def changer(my_list: list[str], data: datetime) -> list[str]:
    """
    Преобразовывает полученный список, исключая те элементы,
    которые не соответствуют полученным паттернам.
    """
    pattern = r"[\d]{1,2}[-\/\. ][\d]{1,2}[-\/\. ][\d]{4}"
    p1 = r"[-\/.]"
    result = []
    for item in my_list:
        match = re.search(pattern, item)
        text = match.group()
        text = re.sub(p1, "/", text)
        try:
            d = datetime.datetime.strptime(text, "%d/%m/%Y")
            delta = data - d
            if delta.days / 365 <= 40 and delta.days / 365 >= 30:
                result.append(item)
        except Exception:
            continue
    return result


def file_writter(filename: str, result_list: list[str]) -> None:
    """
    Записывает в файл данные из списка.
    """
    with open(filename, "w", encoding="utf-8") as file:
        for line in result_list:
            file.write(f"{line}\n")


def main():
    parser = argparse.ArgumentParser(description="Извлечение данных из файла на основе шаблонов.")
    parser.add_argument("readfile", default="data.txt", type=str, help="Путь к файлу для чтения.")
    parser.add_argument("writefile", default="res.txt", type=str, help="Путь к файлу для записи результата.")
    args = parser.parse_args()
    d = datetime.date(2025, 10, 1)
    try:
        file_text = file_open(args.readfile)
        if not file_text:
            raise ValueError(f"Не удалось прочитать данные из файла: {args.readfile}")
        data = datetime.datetime.today()
        result_text = changer(file_text, data)
        print(f"Человек от 30 до 40 лет: {len(result_text)}")
        file_writter(args.writefile, result_text)
        print(f"Результат записан в файл: {args.writefile}")

    except Exception as e:
        print(f"Произошла ошибка: {e}")


if __name__ == "__main__":
    main()