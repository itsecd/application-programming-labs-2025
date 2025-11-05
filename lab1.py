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
    проверка, что имя или фамилия состоит только из букв
    """
    pattern = r'^[А-Яа-яЁё]+$'
    match = re.search(pattern, name)
    return bool(match)


def correct_name (name: str) -> str:
    """
    исправление регистра букв имени или фамилии
    """
    return name[0].upper() + name[1:].lower()


def process_text (text: str) -> str:
    """
    исправление имён и фамилий в анкетах
    """
    pattern = r'^(Фамилия|Имя):\s*(\w+)$'
    lines = text.split('\n')

    for i in range (len(lines)):
        match = re.search(pattern, lines[i])
        if match!=None:
            name = match.group(1)
            value = match.group(2)            
            
            if name == "Фамилия" and is_valid_name(value):
                lines[i] = f"{name}: {correct_name(value)}"
            elif name == "Имя" and is_valid_name(value):
                lines[i] = f"{name}: {correct_name(value)}"
            else:
                print(f"Некорректное значение: {value} в строке {i+1}")
    
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