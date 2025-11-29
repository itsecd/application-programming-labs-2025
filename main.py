# main_lab.py
import os
import sys
from parser import parse_args


def main():

    try:
        args = parse_args()

        if not os.path.exists(args.input):
            raise FileNotFoundError(f"Ошибка: Файл не найден по пути: '{args.input}'")

        if not os.path.isfile(args.input):
            raise ValueError(f"Ошибка: Указанный путь '{args.input}' является директорией, а не файлом.")

        _, ext = os.path.splitext(args.input)

        if ext.lower() != '.csv':
            raise ValueError(f"Ошибка: Файл '{args.input}' имеет некорректное расширение"
                             f"'{args.input}'. Ожидается '.csv'.")

    except FileNotFoundError as e:
        print(e)
        sys.exit(1)
    except ValueError as e:
        print(e)
        sys.exit(1)
    except Exception as e:
        print(f"Произошла непредвиденная ошибка: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()