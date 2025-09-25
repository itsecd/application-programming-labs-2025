import re
import argparse

def file_open(filename:str) -> list[str]:
    """
    принимает имя файла открывает его
    и считывает в список строк
    каждого человека в отдельную строку
    """
    result = []
    person = ""
    text = ""

    try:
        with open(filename, "r", encoding = 'utf-8') as file:
            while True:
                text = file.readline()

                if text == "":
                    result.append(person)
                    break

                if text == "\n" and person:
                    result.append(person)
                    person = ""

                if not re.fullmatch(r"(.{1,3})(\))(\n)", text):
                    person += text

                text = ""
                
        return result  

    except FileNotFoundError:
        print("Error. File not found.")
        return None


def changer(my_list: list[str], pattern: str) -> list[str]:
    """
    Преобразовывает полученный список, исключая те элементы,
    которые не соответствуют полученным паттернам.
    """
    result = []
    for item in my_list:
        if re.search(pattern, item):
            result.append(item)
    return result


def file_writter(filename: str, result_list: list[str]) -> None:
    """
    Записывает в файл данные из списка.
    """
    with open(filename, "w", encoding="utf-8") as file:
        file.writelines(result_list)


def main():
    parser = argparse.ArgumentParser(description="Извлечение данных из файла на основе шаблонов.")
    parser.add_argument("readfile", type=str, help="Путь к файлу для чтения.")
    parser.add_argument("writefile", type=str, help="Путь к файлу для записи результата.")
    args = parser.parse_args()
    
    try:
        file_text = file_open(args.readfile)
        if not file_text:
            raise ValueError(f"Не удалось прочитать данные из файла: {args.readfile}")
            
        pattern1 = r"(0[1-9]|[1-9]|1[0-9]|2[0-2])([\-\/\. ])([9])([\-\/\. ])(1995)"
        pattern2 = r"([\d]{1,2})([\-\/\. ])([1-8]|0[1-8])([\-\/\. ])(1995)"
        pattern3 = r"([\d]{1,2})([\-\/\. ])(0[1-9]|[1-9]|1[0-2])([\-\/\. ])(198[7-9]|199[0-4])"
        pattern4 = r"(2[1-9]|30)([\-\/\. ])([9])([\-\/\. ])(1985)"
        pattern5 = r"([\d]{1,2})([\-\/\. ])(0[1-9]|[1-9]|1[0-2])([\-\/\. ])(1985)"

        pattern = f"({pattern1})|({pattern2})|({pattern3})|({pattern4})|({pattern5})"

        result_text = changer(file_text, pattern)
        print(f"Человек от 30 до 40 лет: {len(result_text)}")
        file_writter(args.writefile, result_text)
        print(f"Результат записан в файл: {args.writefile}")

    except Exception as e:
        print(f"Произошла ошибка: {e}")


if __name__ == "__main__":
    main()