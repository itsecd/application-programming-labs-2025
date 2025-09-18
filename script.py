import os.path
import re
import argparse

def open_and_split(path: str):
    """
    Открытие файла и разбиение анкет на подсписки
    """
    try:
        with open(path,"r",encoding='utf-8') as file:
            text = file.read()
    except FileNotFoundError:
        print(f"файл {path} не найден.")
        return []
    raw_blocks = re.split(r'\n\d+\)\s*', text.strip())[1:]
    group = [i.strip().split('\n') for i in raw_blocks]
    return group



def is_tele(block: list[str])-> str|None:
    """
    поиск строки "Номер или email:"
    """
    for line in block:
        if line.startswith("Номер телефона или email:"):
            part = line.split(':',1)
            return part[1].strip()
    return None

def is_email(value: str)->bool:
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
        r'8\s\(\d{3}\)\s\d{3}-\d{2}-\d{2}',
        r'8\d{10}',
        r'8\s\d{3}\s\d{3}-\d{2}-\d{2}',
        r'8\s\(\d{3}\)\s\d{3}\s\d{2}\s\d{2}',
        r'8\s\d{3}\s\d{3}\s\d{2}\s\d{2}',
        r'^\+7\s\(\d{3}\)\s\d{3}-\d{2}-\d{2}$',
        r'^\+7\d{10}$',
        r'^\+7\s\d{3}\s\d{3}-\d{2}-\d{2}$',
        r'^\+7\s\(\d{3}\)\s\d{3}\s\d{2}\s\d{2}$',
        r'^\+7\s\d{3}\s\d{3}\s\d{2}\s\d{2}$',
    ]
    for pattern in patterns:
        if re.fullmatch(pattern,phone.strip()):
            return True
    return False

def print_and_delete(blocks: list[list[str]])->list[list[str]]:
    """
    вывод некорректных анекет и заполнение списка с правильными
    """

    valid = []
    invalid = []

    for block in blocks:
        value = is_tele(block)
        if value is None:
            invalid.append(block)
            continue
        if is_email(value):
            valid.append(block)
            continue

        if is_valid_num(value):
            valid.append(block)
        else:
            invalid.append(block)

    if invalid:
        print("Некоректные анкеты:")
        for i in range(len(invalid)):
            print(i+1)
            for j in invalid[i]:
                print(j)
            print('\n')
    return valid



def parser_t():
    """
    функция нужна для ввода пути файла
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("path_to_file")

    args = parser.parse_args()
    return args

def save_blocks_to_new_file(blocks:list[list[str]]):
    """
    запрос абсолютного пути для сохранения и само сохранение
    """
    path = input("Введите абсолютный путь для сохранения:")
    try:
        output_path = os.path.join(path,'cleared_data.txt')
        with open(output_path,'w',encoding="utf-8") as f:
            for i,block in enumerate(blocks,1):
                f.write(f"{i})\n")
                f.write("\n".join(block))
                f.write("\n\n")
    except Exception as e:
        print("Ошибка при сохранении файла")


def main():
    a = parser_t()

    input_file = a.path_to_file

    print(f"\nОткрытие файла {input_file}\n")

    list_of_users = open_and_split(input_file)

    cleared_users = print_and_delete(list_of_users)

    save_blocks_to_new_file(cleared_users)

if __name__ == "__main__":
    main()

