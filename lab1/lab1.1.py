import re
import argparse


def get_args():
    """Получение аргументов из командной строки"""
    parser = argparse.ArgumentParser()
    parser.add_argument("in_file", type=str, help="input file")
    parser.add_argument("out_file", type=str, help="output file")
    return parser.parse_args()


def read_file(filename):
    """Чтение содержимого файла"""
    try:
        with open(filename, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"Файл {filename} не найден")
    except Exception as e:
        raise Exception(f"Ошибка при чтении файла: {e}")


def find_moscow(data):
    """Поиск анкет из Москвы"""
    pattern = r"Город:\s*(г\.?\s*)?[Мм]осква\b"
    result = []
    forms = data.split("\n\n")
    
    for form in forms:
        if re.search(pattern, form):
            result.append(form)
    
    return result


def main():
     try:
        args = get_args()
        text = read_file(args.in_file)
        moscow_list = find_moscow(text)
        print(f"Найдено анкет: {len(moscow_list)}")
        for i in moscow_list:
            print(i, sep="/n")
     except Exception as e:
        print(f"Ошибка: {e}")

        
if __name__ == '__main__':
    main()
