#Работа выполнена Кортуновой Анастасией(6211)
import re
import argparse


def date_check(date: str) -> bool:
    """"правильность написания даты по валидным форматам"""
    if (
        re.fullmatch(r"\d\d[./-]\d\d[./-]\d\d\d\d", date)
        or re.fullmatch(r"\d[./-]\d[./-]\d\d\d\d", date)
        or re.fullmatch(r"\d[./-]\d\d[./-]\d\d\d\d", date)
        or re.fullmatch(r"\d\d[./-]\d[./-]\d\d\d\d", date)
    ):
        day, month, year = map(int, re.split(r"[./-]", date))
        if 2025 >= year >= 1900 and 1 <= day <= 31 and 1 <= month <= 12:
            if day == 31 and month not in [1, 3, 5, 7, 8, 10, 12]:
                return False
            if day == 30 and month == 2:
                return False
            if month == 2 and day > 28:
                return False
            return True
    return False


def email_check(email: str) -> bool:
    """"правильность написания почты по валидным форматам"""
    if email[email.find("@") + 1 : -1] in ["gmail.com", "mail.ru", "yandex.ru"]:
        if re.fullmatch(r"[A-Za-z0-9._%+-]{,64}", email[: email.find("@")]):
            return True
    return False


def phone_check(phone: str) -> bool:  #!! +7 или 8 в одну строку плохо работало
    """"правильность написания номера телефона по валидным форматам"""
    if re.fullmatch(
        r"8\s?\(?\d{3}\)?\s?\d{3}[\s-]?\d{2}[\s-]?\d{2}", phone
    ) or re.fullmatch(r"\+7\s?\(?\d{3}\)?\s?\d{3}[\s-]?\d{2}[\s-]?\d{2}", phone):
        return True
    return False


def town_check(town: str) -> bool:
    """"правильность написания города по валидным форматам"""
    if re.fullmatch(
        r"г\.\s?[А-ЯЁ][а-яё]+|[А-ЯЁ][а-яё]+", town
    ) or re.fullmatch(r"[А-ЯЁ][а-яё]+|[А-ЯЁ][а-яё]+", town):
        return True
    return False


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("file", type=str, help="Введите путь до файла")
    parser.add_argument("name", type=str, help="Введите имя")
    args = parser.parse_args()      #обработка аргументов командной строкии сохранение в args
    file_to_open = args.file      
    curr_name = args.name
    if (
        curr_name is not None and file_to_open is not None
    ):  # проверка были ли переданы аргументы в cmd
        try:
            data = ""
            with open(file_to_open, "r", encoding="utf-8") as file:
                data = file.readlines()
            mode = 0                              # режим обработки данных(чтобы знать проверяем фамил,имя,дату или телефон)
            is_valid = True                       # следит, является ли строка данных допустимой
            count = 0                             # подсчет кол-ва успешно обработ. анкет
            user = []                             # анкета пустая
            result_str = ""                       # прстроение итоговой строки о всех успешных анкетах
            for string in data:
                if re.fullmatch(r"\d+[)]\n", string) or string == "\n":  #проверка первой строки с числом
                    mode = 0                                             #сброс в 0(начинает работу с новой анкетой)
                    user.clear()                                         #!!Очищаем, что успели сохранить и начинаем новую запись
                    is_valid = True                                      # пока еще анкета допустимого формата 
                    continue
                if is_valid == False:
                    continue
                string = string[string.find(":") + 2 : -1]               
                match mode:
                    case 0:
                        is_valid = string[0].isupper()
                    case 1:
                        is_valid = string[0].isupper()
                    case 2:
                        is_valid = string in [
                            "М",
                            "м",
                            "Мужской",
                            "мужской",
                            "Ж",
                            "ж",
                            "Женский",
                            "женский",
                        ]
                    case 3:
                        is_valid = date_check(string)
                    case 4:
                        is_valid = phone_check(string) or email_check(string)  #!!
                    case 5:
                        is_valid = town_check(string)

                if is_valid:  #!!
                    user.append(string)  # Сохраняем чтоб потом записать анкету в файл

                mode += 1

                if (
                    mode == 6 and is_valid and curr_name == user[1]
                ):  # !! Подходит и все данные верные
                    # !! Тут сохранение в файл
                    count += 1
                    result_str += f"""{count})
Фамилия: {user[0]}
Имя: {user[1]}
Пол: {user[2]}
Дата рождения: {user[3]}
Номер телефона или email: {user[4]}
Город: {user[5]}\n\n"""  #!! Итоговая строка которую потом запишем в файл


            with open("result.txt", "w", encoding="utf-8") as res:   #with обеспечивает закрытие файла после завершения работы(res для обращения к файлу)
                res.write(result_str)
            print(f"Количество людей по имени {curr_name} = {count}")

        except FileExistsError:                                      #обработка исключений(если файл пытаются открыть, а он не существует)
            print(f"Ошибка: Файл '{file_to_open}' не найден ")
        except Exception as e:                                       #перехватывает любые другие исключения
            print(f"Произошла ошибка при работе с файлом: {e}")
    else:
        print("Запустите python main.py имя_файла имя_человека!")


if __name__ == "__main__":                          #гарантия, что main вызовется при запуске скрипта
    main()

