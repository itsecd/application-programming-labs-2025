import re
import argparse

def open_file(filename_1:str,filename_2:str):
    """
    открытие файла
    """
    try:
        with open(filename_1, "r", encoding="utf-8") as file:
            text = read_file(file,filename_2)
            return text
    except FileNotFoundError:
        raise FileNotFoundError("Файл не найден")

def read_file(file,filename_2:str):
    """
    чтение содержимого и
    запись в другой файл
    """
    content=file.read()
    ankets = re.findall(r'\d+\)\n(?:.*\n)+?(?=\d+\)|$)', content)
    moscow=[]
    for anketa in ankets:
        if re.search(r"Город:\s*[г.\s*]Москва",anketa):
            moscow.append(anketa)
    quantity=len(re.findall("Москва",content))
    with open(filename_2, "w", encoding="utf-8") as file_1:
        for anketa in moscow:
            file_1.write(anketa)
    return quantity

def parsing():
    """
    передача аргументов через командную строку
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', type=str,help="Введите путь файла")
    parser.add_argument('filenameoutput', type=str,help="Введите путь файла для вывода")
    args= parser.parse_args()
    return args.filename, args.filenameoutput

def main()->None:
    filename_1,filename_2=parsing()
    print(open_file(filename_1,filename_2))

if __name__ == "__main__":
    main()