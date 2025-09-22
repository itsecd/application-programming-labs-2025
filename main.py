import argparse
import re


def correct_number(text) -> re.Match:
    """
    Проверка совпадения номера по заданному шаблону.
    """

    pattern1 = r"^Номер телефона или email: (\+7|8)\d{10}$"
    pattern2 = r"^Номер телефона или email: (\+7|8)( \(\d{3}\) )\d{3}[ -]{1}\d{2}[ -]\d{2}$"
    pattern3 = r"^Номер телефона или email: (\+7|8)( \d{3} )\d{3}[ -]{1}\d{2}[ -]\d{2}$"
    return re.match(pattern1, text) or re.match(pattern2, text) or re.match(
        pattern3, text)


def read_file(file_path) -> str:
    """
    Чтения файла, если это возможно.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as rfile:
            return rfile.read()
    except FileNotFoundError as e:
        raise


def result_output(count, path) -> None:
    """
    Вывод в консоль результата программы.
    """
    print(f"\nКоличество корректных номеров среди анкет: {count}")
    print(f"Все подходящие анкеты записаны в \"{path}\"\n")


def parse_args_console() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--read_file",
                        "-rf",
                        type=str,
                        help="path to read file")
    parser.add_argument("--write_file",
                        "-wf",
                        type=str,
                        help="path to write file")
    return parser.parse_args()


def main():
    args = parse_args_console()

    write_path = args.write_file if (args.write_file
                                     is not None) else "result.txt"

    count_correct_numbers = 0
    if args.read_file is not None:
        text = read_file(args.read_file)
        text = text.splitlines()  # Превращаем текст в список строк
        with open(write_path, "w", encoding="utf-8") as wfile:
            for i in range(len(text)):  # Двигаемся по списку через индексы
                if (correct_number(
                        text[i])):  # Проверяем удовл. ли номер паттерну
                    print(type(correct_number(text[i])))
                    count_correct_numbers += 1
                    # Нужно отойти на 4 строчки назад и 1 вперед, чтобы сохранить анкету
                    # с самого начала
                    wfile.write("\n" + str(count_correct_numbers) + ")\n")
                    for x in range(-4, 2):
                        wfile.write(text[i + x] + '\n')

        result_output(count_correct_numbers, write_path)


if __name__ == "__main__":
    main()
