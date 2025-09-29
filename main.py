def factor(parlst: list) -> bool:

    if name(parlst[0]):
        if name(parlst[1]):
            if gender(parlst[2]):
                if city(parlst[5]):
                    if date(parlst[3]):
                        if num_mail(parlst[4]):
                            return True

    return False

def name(text: str) -> bool:
    """
        проверка фамилии и имени
    """
    try:
        text = text.split(' ')[1]
    except:
        print("Ошибка 2! Введен файл неправильного вида!")
    return text[0].upper() == text[0]

def gender(text: str) -> bool:
    """
        проверка пола
    """
    try:
        text = text.split(' ')[1]
    except:
        print("Ошибка 3! Введен файл неправильного вида!")
    return text in ["м","М","ж","Ж","мужской","Мужской","женский","Женский",]

def date(text: str) -> bool:
    """
        проверка даты рождения
    """
    try:
        text = text.split(' ')[2]
    except:
        print("Ошибка 4! Введен файл неправильного вида!")

    # разделение по знакам
    if '.' in text:
        text = text.split('.')
    elif '-' in text:
        text = text.split('-')
    elif '/' in text:
        text = text.split('/')
    else:
        return False

    # года
    if int(text[2]) < 2000:
        return False

    # месяца
    if int(text[1]) < 0 or int(text[1]) > 12:
        return False

    # дни
    d31 = [1,3,5,7,8,10,12]
    d30 = [4,6,9,11]
    if int(text[0]) < 0:
        return False
    if int(text[1]) in d31 and int(text[0]) > 31:
        return False
    if int(text[1]) in d30 and int(text[0]) > 30:
        return False
    if int(text[1]) == 2 and int(text[0]) > 28:
        return False

    #сегодня
    if int(text[0]) > 29 and int(text[1]) == 9 and int(text[2]) == 2025:
        return False
    if int(text[1]) > 9 and int(text[2]) == 2025:
        return False
    if int(text[2]) > 2025:
        return False
    return True

def num_mail(text: str) -> bool:
    """
        проверка номера телефона или почты
    """

    try:
        text = "".join(text.split(' ')[4:])
    except:
        print("Ошибка 5! Введен файл неправильного вида!")

    # почта
    if '@' in text:
        text = text.split('@')
        alt_text = text[0].lower()
        alph = "qwertyuiopasdfghjklzxcvbnm1234567890_%+-"
        if len(text) != 2 or not text[1] in ["gmail.com", "mail.ru", "yandex.ru"] or len(text[0]) > 64:
            return False
        for i in range(0,len(alt_text)):
            if not alt_text[i] in alph:
                return False

    # номер телефона
    elif text[0] in ['8','+']:

        # проверка на символ -
        if text.count('-') > 0:
            if text.count('-') != 2:
                return False
            elif text[-3] != '-' or text[-6] != '-':
                return False

        # проверка на ()
        if text.count('(') != text.count(')'):
            return False
        if text.count('(') > 0:

            if text.count('(') != 1:
                return False

            if text[0] == '8' and (text[1] != '(' or text[5] != ')'):
                return False
            elif text[0] == '+' and (text[2] != '(' or text[6] != ')'):
                return False

        # проверка на кол-во цифр
        c = 0
        for i in range(0,len(text)):
            if text[i].isdigit():
                c+=1
        if c != 11:
            return False
    else:
        return False

    return True

def city(text: str) -> bool:
    """
        проверка города
    """

    try:
        text = text.split(' ')[1:]
    except:
        print("Ошибка 6! Введен файл неправильного вида!")
    if text[0] == "г.":
        text = text[1:]
    return text[0][0].upper() == text[0][0]

def main():

    result = 0

    read_file_name = input("введите названия читаемого файла: ")
    try:
        data = open(read_file_name, "r", encoding="utf-8")
        data.close()
    except:
        print("Ошибка в вводе имени читаемого файла!")
        return

    write_file_name = input("введите названия записываемого файла: ")
    try:
        data = open(write_file_name, "r", encoding="utf-8")
        data.close()
    except:
        print("Ошибка в вводе имени записываемого файла!")
        return

    with open(read_file_name, "r", encoding="utf-8") as data, open(write_file_name, 'w', encoding="utf-8") as new_data:
        while True:
            full_line = ""
            while True:
                line = data.readline()
                if not line or line == '\n':
                    break
                full_line += '|' + line.strip()

            lst = full_line.split('|')

            try:
                lst = lst[2:]
            except:
                print("Ошибка 1! Введен файл неправильного вида!")

            if factor(lst):
                result += 1
                new_data.writelines([str(result), ")\n", lst[0], '\n', lst[1], '\n', lst[2], '\n', lst[3], '\n', lst[4], '\n', lst[5], "\n\n"])

            if not line:
                break

    print("количество людей родившихся в 21 веке:", result)


if __name__ == "__main__":
    main()
