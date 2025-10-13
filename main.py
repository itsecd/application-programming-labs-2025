import argparse
import re

def correct_numbers(text: str) -> list:
    """
    Извлекает анкеты с номерами телефона в заданных форматах.
    """
    pattern = r"(\d+\)\n.*?Номер телефона или email: (?:\+7\s?(?:\d{3}|\(\d{3}\))[\s-]?\d{3}[\s-]?\d{2}[\s-]?\d{2}|8\s?(?:\d{3}|\(\d{3}\))[\s-]?\d{3}[\s-]?\d{2}[\s-]?\d{2})\n.*?)\n"
    return re.findall(pattern, text, re.DOTALL)

def read_file(file_path: str) -> str:
    """
    Чтения файла, если это возможно.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as rfile:
            return rfile.read()
    except FileNotFoundError as e:
        raise


def result_output(count: int , path: str) -> None:
    """
    Вывод в консоль результата программы.
    """
    print(f"\nКоличество корректных номеров среди анкет: {count}")
    print(f"Все подходящие анкеты записаны в \"{path}\"\n")


def parse_args_console() -> argparse.Namespace:
    """
    Парсинг параметров с консоли.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("--read_file",
                        "-rf",
                        type=str,
                        help="path to read file")
    parser.add_argument("--write_file",
                        "-wf",
                        type=str,
                        default="result.txt",
                        help="path to write file")
    return parser.parse_args()


def main():
    args = parse_args_console()
    write_path = args.write_file
    # write_path = args.write_file if (args.write_file
    #                                  is not None) else "result.txt"
    if args.read_file is not None:
        text = read_file(args.read_file)
        with open(write_path, "w", encoding="utf-8") as wfile: 
            forms = correct_numbers(text)
            for form in forms:
                
                wfile.write(str(form) + "\n")

        result_output(len(forms), write_path)


if __name__ == "__main__":
    main()
