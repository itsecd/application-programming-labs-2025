import re
import argparse
import os

import parser as my_parser

# Найдите анкеты людей, у которых указана почта (в корректном формате).
# Выведите их количество на экран и сохраните найденные анкеты в новый файл.


# Функция для записи данных в файл
def write_to_file(output_filename: str, data) -> None:
    """
    function for adding a record to a file
    """
    try:
        with open(output_filename, "a", encoding="utf-8") as file:
            file.write(data)
            if data and not data.endswith("\n"):
                file.write("\n")
            file.write("\n")
    except FileNotFoundError:
        raise FileNotFoundError("file not exists")


# 
def clear_output_file(output_filename: str) -> bool:
    """
    Очистка файла вывода перед началом обработки
    """
    try:
        with open(output_filename, "w", encoding="utf-8") as file:
            file.write("")
        return True
    except FileNotFoundError:
        raise FileNotFoundError("Output file not exists")
    except Exception as e:
        raise Exception(f"An error occurred while clearing the output file: {e}")


# Чтение одной анкеты из файла
def read_next_anketa(file, lines_per_anketa: int = 7) -> str:
    """
    Reads the next anket from the file.
    Returns the anket data as a string, or an empty string if EOF is reached.
    """
    data = ""
    for _ in range(lines_per_anketa):  # Считывает 7 строк (предполагаемый формат записи)
        line = file.readline()
        if not line:
            break
        data += line

    return data


# Обработка и фильтрация анкет
def process_and_filter_ankets(
    data_filename: str, output_filename: str
) -> tuple[bool, int]:
    """
    Processes the input file, filters anketas by valid email, and writes them to the output file.
    Returns a tuple (success: bool, count: int).
    """
    # Очистка файла вывода перед началом обработки
    if not clear_output_file(output_filename):
        return False, 0

    try:
        with open(data_filename, "r", encoding="utf-8") as file:
            count = 0
            while True:
                data = read_next_anketa(file)
                if not data.strip():  # Если данные пусты, выходим из цикла
                    break

                # Парсит данные в словарь
                user = my_parser.parse_data(data)
                if my_parser.valid_user(
                    user
                ):  # Проверяет, есть ли у пользователя валидный email
                    pattern = r"\d+[)]"  # Находит и заменяет номер в скобках
                    # count=1 для замены только первого вхождения
                    updated_data = re.sub(pattern, str(count + 1) + ")", data, count=1)
                    write_to_file(output_filename, updated_data)
                    count += 1
                file.readline()  # Пропускает пустую строку между записями
        return True, count
    except FileNotFoundError:
        raise FileNotFoundError("Input file not exists")
    except Exception as e:
        raise Exception(f"An error occurred during file processing: {e}")
    
    
# Основная функция обработки данных
def main():
    """
    Main function to handle command line arguments and orchestrate the process.
    """
    try:
        # Получаем аргументы командной строки
        data_filename, output_filename = cli_get_args()

        success, count = process_and_filter_ankets(data_filename, output_filename)

        if success:
            print(f"count user with email: {count}")
            print("the program has finished")
            exit(0)
        print("somthing error :(")
        exit(1)
    except Exception as ex:
        print(ex)


# Получение аргументов командной строки
def cli_get_args() -> tuple[str, str]:
    """
    receives arguments from the command line
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-fn", "--filename", type=str, help="your filename", default="data.txt"
    )  # Аргумент: имя входного файла data.txt
    parser.add_argument(
        "-o", "--output", type=str, help="output filename", default="output.txt"
    )  # Аргумент: имя выходного файла output.txt
    args = parser.parse_args()

    data_filename = os.path.basename(args.filename)
    output_filename = os.path.basename(args.output)

    return data_filename, output_filename


if __name__ == "__main__":
    main()
