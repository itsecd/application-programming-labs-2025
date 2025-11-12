import argparse
import sys
import re 

def fopen() -> list:
    parser = argparse.ArgumentParser()
    parser.add_argument('path', type=str)
    arg = parser.parse_args()
    try:
            with open(arg.path, 'r', encoding='utf-8') as file:
                lines = file.readlines()
    except FileNotFoundError as er:
            print(er, " Неверное название файла")
            sys.exit(1)
    return [line for line in lines if line.strip()]

def check(text: list) -> bool:
    """
    Функция проверки, правильно ли заполнены поля "пол"
    Если поле заполнено неправильно, выведет, его номер
    """
    ''' Регулярное выражение для проверки поля "Пол" '''
    pattern = r'^(М|м|Мужской|мужской|Ж|ж|Женский|женский)$'

    num = 0
    Errnum = 0
    for i in range(3, len(text), 7):
        gender_line = text[i]
        num += 1
        try:
            gender = gender_line.split(": ", 1)[1].strip()
        except IndexError:
            Errnum += 1
            print(" Ошибка в формате анкеты №", num)
            continue

        """
        Проверяем с помощью регулярного выражения 
        """
        if not re.match(pattern, gender):
            print("В строке ", num, " Ошибка в записи пола\n")
            Errnum += 1

    if Errnum != 0:
        return False
    return True

def men() -> int:
    """
    Функция для поиска всех мужских анкет, записи их в новый файл
    """
    f = open("new_data.txt", 'w', encoding='utf-8')
    cntr = 0
    text = fopen()
    if check(text) == False:
        return 0 
    for i in range(3, len(text), 7):
        text[i] = text[i].split(": ", 1)[1].strip()
        if re.match(r'^(М|м|Мужской|мужской)$', text[i]):
            cntr += 1
            f.writelines([
                text[i - 3],
                text[i - 2],
                text[i - 1],
                'Пол: ' + text[i] + '\n',
                text[i + 1],
                text[i + 2],
                text[i + 3] + '\n',
            ])
    f.close()
    return cntr

if __name__ == '__main__':
    result = men()
    print("Количество мужских анкет: ", result)