import re

def is_surname(line: str) -> bool:
    '''Проверяет, соответстует ли строка формату Фамилии'''
    return re.fullmatch(r"Фамилия: [А-Я, Ё][а-я,ё]*", line) is not None

def is_name(line: str) -> bool:
    '''Проверяет, соответстует ли строка формату Имя'''
    return re.fullmatch(r"Имя: [А-Я,Ё][а-я,ё]*", line) is not None
    
def is_data(line: str) -> bool:
    '''Проверяет, соответстует ли строка формату даты рождения'''
    match = re.fullmatch(r"Дата рождения: (\d{1,2})([-./])(\d{1,2})\2(\d{4})", line)
    
    if not match:
        return False
    
    day, month, year = map(int, [match.group(1), match.group(3), match.group(4)])
    
    if month < 1 or month > 12:
        return False
    if day < 1 or day > 31:
        return False
    if year < 1900 or year>2025:
        return False
    
    days_in_month = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    if day > days_in_month[month - 1]:
        return False
    
    if month == 2 and day == 29:
        if not (year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)):
            return False
    
    return True
       
def is_gender(line: str) -> bool:
    '''Проверяет, соответстует ли строка формату Пола'''
    return re.fullmatch(r"Пол:[Мм]ужской|[Мм]|[Жж]енский|[Жж]", line) is None

def is_contact(line: str) -> bool:
    '''Проверяет, соответстует ли строка формату номера Телефона или Email '''
    phone_number = re.fullmatch(r"Номер телефона или email: (\+7|8)[\s(-]*(\d{3})[\s)]*(\d{3})([\s)-]*)(\d{2})\4(\d{2})", line)
    if phone_number:
        number = re.findall(r"\d", line)
        if len(number) == 11:
            return True
    mail = re.fullmatch(r"Номер телефона или email: [A-Za-z0-9._%+-]{1,64}@(gmail\.com|mail\.ru|yandex\.ru)", line)
    email_part = line.replace("Номер телефона или email: ", "")
    if len(email_part) <= 64:
        return True
    
    return False

def is_city(line: str) -> bool:
    '''Проверяет, соответстует ли строка формату Города'''
    return re.fullmatch( r"Город:\s*(г\.\s*)?[А-ЯЁ][а-яё]+(?:[- ][А-ЯЁ]?[а-яё]+)*", line) is not None

