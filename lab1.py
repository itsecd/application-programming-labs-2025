import re
import argparse


def read_file (file_name: str) -> str:
    """
    чтение из файла
    """
    with open(file_name, "r", encoding="utf-8") as file:
        text = file.read()
        return text


def write_file (text: str, output_file: str) -> None:
    """
    запись в файл
    """
    with open(output_file, "w", encoding="utf-8") as file:
        file.write(text)


def is_valid_name (name: str) -> bool:
    """
    проверка, что имя состоит только из букв
    """
    pattern = r'^[А-Яа-я]+$'
    match = re.search(pattern, name)
    return bool(match)


def is_valid_surname (surname: str) -> bool:
    """
    проверка, что фамилия состоит только из букв
    """
    pattern = r'^[А-Яа-я]+$'
    match = re.search(pattern, surname)
    return bool(match)


def correct_name (name: str) -> str:
    """
    исправление регистра букв имени
    """
    return name[0].upper() + name[1:].lower()


def correct_surname (surname: str) -> str:
    """
    исправление регистра букв фамилии
    """
    return surname[0].upper() + surname[1:].lower()


def process_text (text: str) -> str:
    """
    исправление имён и фамилий в анкетах
    """
    lines = text.split('\n')

    for i in range (len(lines)):
        if lines[i].startswith("Фамилия:"):
            parts_of_lines = lines[i].split(':')
            surname = parts_of_lines[1].strip()
            if is_valid_surname(surname):
                lines[i] = f"{parts_of_lines[0]}: {correct_surname(surname)}"
    
        elif lines[i].startswith("Имя:"):
            parts_of_lines = lines[i].split(':')
            name = parts_of_lines[1].strip()
            if is_valid_name(name):
                lines[i] = f"{parts_of_lines[0]}: {correct_name(name)}"
    
    correct_text = '\n'.join(lines)
    return correct_text   


def main() :

    parser = argparse.ArgumentParser()
    parser.add_argument("-i", '--input_file_name', type=str, default='data.txt', help='name of input file')
    parser.add_argument("-o", '--output_file_name', type=str, default='output.txt', help='your name of output file')
    args = parser.parse_args()
    print(f"The name of input file is: {args.input_file_name}")
    print(f"The name of output file is: {args.output_file_name}")

    try:
        write_file(process_text(read_file(args.input_file_name)), args.output_file_name)
    except FileNotFoundError:
        print("Ошибка: файл не найден")


if __name__ == "__main__" :
    main()