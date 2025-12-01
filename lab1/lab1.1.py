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


def main():
     try:
        args = get_args()
        text = read_file(args.in_file)
        print(text)
        print(f"Файл успешно прочитан, размер: {len(data)} символов")
     except Exception as e:
        print(f"Ошибка: {e}")

        
if __name__ == '__main__':
    main()
