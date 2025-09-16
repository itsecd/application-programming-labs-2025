import re

#TODO add argparse instead of 'data.txt'
with open('data.txt', 'r', encoding='utf-8') as file:
    content = file.readlines()

    lst1 = []

    #TODO figure how not to add not fully populated dict
    tmp_dct = {}
    for line in content:
        match = re.search(r"^\d+", line)
        if match:
            tmp_dct.update({"ID": match.group()})
        match = re.findall(r"Фамилия:\s+([А-ЯЁ]+[а-яё]+)", line)
        if match:
            tmp_dct.update({"Фамилия": match[0]})
        match = re.findall(r"Имя:\s+([А-ЯЁ]+[а-яё]+)", line)
        if match:
            tmp_dct.update({"Имя": match[0]})
        match = re.findall(r"Пол:\s+(М$|м$|Мужской$|мужской$|Ж$|ж$|Женский$|женский$)", line)
        if match:
            tmp_dct.update({"Пол": match[0]})

        #TODO add age, mobile, city
        match = re.findall(r"Дата рождения:\s+(\d{})", line)
        if match:
            tmp_dct.update({"Дата рождения": match[0]})

        match = re.fullmatch("\n", line)
        if match:
            lst1.append(tmp_dct.copy())
            tmp_dct.clear()

    for line in lst1:
        print(line)

    #TODO var7: Найдите всех людей, чьи телефоны имеют код города 927. Выведите их количество на экран и сохраните их анкеты в новый файл.