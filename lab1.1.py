import argparse
import re

def openfile()->list[str]:
    """
    Функция для чтения из файла
    С помощью argarce мы передаем имя файла как аргумент командной строки
    Далее делаем проверку и закрываем файл
    """
    parser = argparse.ArgumentParser()  
    parser.add_argument('file', type=str, help='file')  
    args = parser.parse_args()
    try:
        file = open(args.file, 'r', encoding='utf-8')
    except FileNotFoundError as exs:
        print(f"Error: {exs}")
        return None
    
    text = file.read()
    file.close()
    return text