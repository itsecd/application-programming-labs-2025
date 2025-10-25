import argparse
import re


def read_file(path: str) -> str:
    """
    Читает содержимое файла. Выбрасывает исключение, если файл не найден
    """
    try:
        with open(path, "r", encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"Файл {path} не найден.")


def split_into_blocks(text: str) -> list[list[str]]:
    """
    Разбивает текст на блоки анкет и возвращает список списков строк
    """
    raw_blocks = re.split(r'\n\d+\)\s*', text.strip())[1:]
    return [block.strip().split('\n') for block in raw_blocks]


def open_and_split(path: str) -> list[list[str]]:
    """
    Открытие файла и разбиение анкет на подсписки
    """
    text = read_file(path)
    return split_into_blocks(text)


def get_tele_or_email(block: list[str])-> str|None:
    """
    поиск строки "Номер или email:"
    """
    for line in block:
        if line.startswith("Номер телефона или email:"):
            part = line.split(':',1)
            return part[1].strip()
    return None


def is_email(value: str) -> bool:
    """
    проверка, что найденная строка не явл. email
    """
    if '@' in value:
        pattern = r'^[a-zA-Z0-9а-яА-Я._%+-]+@[a-zA-Z0-9а-яА-Я.-]+\.[a-zA-ZА-Яа-я]{2,}$'
        return bool(re.fullmatch(pattern, value.strip()))
    pattern = r'^[a-zA-Z0-9а-яА-Я]+\.([a-zA-Z0-9а-яА-Я]+\.)+[a-zA-ZА-Яа-я]{2,}$'
    return bool(re.fullmatch(pattern, value.strip()))


def is_valid_num(phone:str) ->bool:
    """
    проверка номера по форматам
    """
    patterns=[
         r'^(?:\+7|8)\d{10}$',  # сплошной номер
        r'^(?:\+7|8)(?:\s?\(\d{3}\)|\s\d{3})\s?\d{3}[\s-]?\d{2}[\s-]?\d{2}$'  # форматированный
    ]
    for pattern in patterns:
        if re.fullmatch(pattern,phone.strip()):
            return True
    return False


def print_invalid(blocks: list[list[str]])-> None:
	"""
	вывод некорректных анкет
	"""
	print("Некоректные анкеты:")
        for i in range(len(invalid)):
            print(i+1)
            for j in invalid[i]:
                print(j)
            print('\n')


def make_valid_txt_and_print_invalid(blocks: list[list[str]])->list[list[str]]:
    """
    вывод некорректных анекет и заполнение списка с правильными
    """
    valid = []
    invalid = []

    for block in blocks:
        value = get_tele_or_email(block)
        if value is None:
            invalid.append(block)
            continue
        if is_not_email(value):
            valid.append(block)
            continue

        if is_valid_num(value):
            valid.append(block)
        else:
            invalid.append(block)

    if invalid:
       print_invalid(invalid)
    return valid



def parser_t():
    """
    функция нужна для ввода пути файла
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("path_to_file")
    parser.add_argument(
        "-o", "--output",
        help="Путь для сохранения очищенного файла",
        default="cleared_data.txt"
    )
    return parser.parse_args()


def save_blocks_to_new_file(blocks: list[list[str]], output_path: str):
    """
    запрос абсолютного пути для сохранения и само сохранение
    """
    with open(output_path, 'w', encoding="utf-8") as f:
        for i, block in enumerate(blocks, 1):
            f.write(f"{i})\n")
            f.write("\n".join(block))
            f.write("\n\n")


def main():
    a = parser_t()

    input_file = a.path_to_file
    output_path = a.output

    print(f"\nОткрытие файла {input_file}\n")

    try:
        list_of_users = open_and_split(input_file)
        cleared_users = print_and_delete(list_of_users)
        save_blocks_to_new_file(cleared_users, output_path)
    except Exception as e:
        print("Ошибка: ", e)


if __name__ == "main":
    main()