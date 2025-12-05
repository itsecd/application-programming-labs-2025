import re
from validators import is_surname, is_name, is_gender, is_data, is_contact, is_city

def process_surname(line: str) -> str:
    '''Обрабатывает строку с фамилией.'''
    return line if is_surname(line) else "Фамилия: -"


def process_name(line: str) -> str:
    '''Обрабатывает строку с именем.'''
    return line if is_name(line) else "Имя: -"


def process_gender(line: str) -> str:
    '''Обрабатывает строку с полом.'''
    if is_gender(line):
        if line[5] in ("М", "м"):
            return "Пол: М"
        else:
            return "Пол: Ж"
    return "Пол: -"


def process_birth_date(line: str) -> str:
    '''Обрабатывает строку с датой рождения.'''
    if is_data(line):
        match = re.match(r"Дата рождения: (\d{1,2})[-./](\d{1,2})[-./](\d{4})", line)
        if match:
            day, month, year = match.groups()
            formatted_day = day.zfill(2)
            formatted_month = month.zfill(2)
            return f"Дата рождения: {formatted_day}.{formatted_month}.{year}"
    return "Дата рождения: -"


def process_contact(line: str) -> str:
    '''Обрабатывает строку с контактными данными.'''
    if is_contact(line):
        phone_pattern = r"Номер телефона или email: (\+7|8)[\s(-]*(\d{3})[\s)]*(\d{3})([\s)-]*)(\d{2})\4(\d{2})"
        phone_match = re.fullmatch(phone_pattern, line)
        
        if phone_match:
            contact_text = phone_match.group()
            cleaned_contact = re.sub(r"[\s\-\(\)]", "", contact_text)
            phone_number = re.sub(r"Номертелефонаилиemail:", "", cleaned_contact)
            phone_number = re.sub(r"\+7", "8", phone_number)
            return f"Номер телефона или email: {phone_number}"

        return line
    return "Номер телефона или email: -"


def process_city(line: str) -> str:
    '''Обрабатывает строку с городом.'''
    
    if is_city(line):
        
        city_pattern = r"Город:\s*(г\.\s*)[А-ЯЁ][а-яё]+(?:[- ][А-ЯЁ]?[а-яё]+)*"
        city_match = re.fullmatch(city_pattern, line)
        
        if city_match:
            city_text = city_match.group()
            cleaned_city = re.sub(r"г\.\s*", "", city_text)
            return cleaned_city
        
        return line
    
    return "Город: -"


def process_lines(lines: str) -> str:
    '''Обрабатывает все строки данных.'''
    processed_lines = []
    processed_lines.append(lines[0])
    i = 1
    count_lines = len(lines)
    while i < count_lines:
        if i < count_lines:
            processed_lines.append(lines[i])
            i += 1
        
        if i < count_lines:
            processed_lines.append(process_name(lines[i]))
            i += 1
        
        if i < count_lines:
            processed_lines.append(process_gender(lines[i]))
            i += 1
        
        if i < count_lines:
            processed_lines.append(process_birth_date(lines[i]))
            i += 1
        
        if i < count_lines:
            processed_lines.append(process_contact(lines[i]))
            i += 1
        
        if i < count_lines:
            processed_lines.append(process_city(lines[i]))
            i += 1
        
        if(count_lines-i>1):
            for j in range(0,2):
                processed_lines.append(lines[i])
                i += 1
    
    return processed_lines