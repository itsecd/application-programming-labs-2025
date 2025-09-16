#Работа выполнена Кортуновой Анастасией(6211)
import argparse
import re

def date_check(date: str) -> bool:
    """Функция проверяет корректность указанной даты в анкете"""
    if not re.fullmatch(r"\d{1,2}[./-]\d{1,2}[./-]\d{4}", date):
        return False
    
    day, month, year = map(int, re.split(r"[./-]", date))
    
    if not (1900 <= year <= 2025 and 1 <= month <= 12 and 1 <= day <= 31):
        return False
    if day == 31 and month not in [1, 3, 5, 7, 8, 10, 12]:
        return False
    if month == 2 and day >28 :
            return False
    return True


def email_check(email: str) -> bool:
    """Функция проверяет корректность указанной почты в анкете"""
    if not re.fullmatch(r"[A-Za-z0-9._%+-]{1,64}@(gmail\.com|mail\.ru|yandex\.ru)", email):
        return False
    return True


def phone_check(phone: str) -> bool:  
    """Функция проверяет корректность указанного номера телефона в анкете"""
    pattern = r"(?:8|\+7)\s?\(?\d{3}\)?\s?\d{3}[\s-]?\d{2}[\s-]?\d{2}"
    return bool(re.fullmatch(pattern, phone))


def town_check(town: str) -> bool:
    """Функция проверяет корректность указанного города в анкете"""
    pattern = r"(?:г\.\s?)?[А-ЯЁ][а-яё]+"
    return bool(re.fullmatch(pattern, town))


def validate_field(mode: int, value: str) -> bool:
    """Проверяет поле в зависимости от его типа"""
    match mode:
        case 0 | 1:  # Фамилия и имя
            return value[0].isupper()
        case 2:      # Пол
            return value.lower() in ["м", "мужской", "ж", "женский"]
        case 3:      # Дата рождения
            return date_check(value)
        case 4:      # Телефон или email
            return phone_check(value) or email_check(value)
        case 5:      # Город
            return town_check(value)
        case _:
            return False
        

def process_user_data(user: list, curr_name: str, count: int) -> tuple[int, str]:
    """Обрабатывает данные пользователя и формирует результат"""
    if curr_name == user[1]:
        count += 1
        result_str = f"""{count})
Фамилия: {user[0]}
Имя: {user[1]}
Пол: {user[2]}
Дата рождения: {user[3]}
Номер телефона или email: {user[4]}
Город: {user[5]}\n\n"""
        return count, result_str
    return count, ""


def parse_arguments():
    """Парсит аргументы командной строки"""
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file", type=str, help="Введите путь до файла")
    parser.add_argument("name", type=str, help="Введите имя для поиска в анкетах")
    parser.add_argument("output_file", type=str, help="Введите путь до файла для записи результатов")
    return parser.parse_args()


def read_input_file(filename: str):
    """Читает данные из входного файла"""
    try:
        with open(filename, "r", encoding="utf-8") as file:
            return file.readlines()
    except FileNotFoundError:
        raise FileNotFoundError(f"Файл '{filename}' не найден")
    except Exception as e:
        raise Exception(f"Ошибка при чтении файла: {e}")
    

def write_output_file(filename: str, content: str):
    """Записывает результаты в выходной файл"""
    try:
        with open(filename, "w", encoding="utf-8") as file:
            file.write(content)
    except Exception as e:
        raise Exception(f"Ошибка при записи файла: {e}")
    

def process_ankets_data(data: list, target_name: str) -> tuple[int, str]:
    """Обрабатывает все анкеты и возвращает результаты"""
    mode = 0
    is_valid = True
    count = 0
    user = []
    result_content = ""
    
    for line in data:
        # Сброс при новой анкете или пустой строке
        if re.fullmatch(r"\d+[)]\n", line) or line == "\n":
            mode = 0
            user.clear()
            is_valid = True
            continue
        
        if not is_valid:
            continue
        
        # Извлекаем значение поля
        field_value = line[line.find(":") + 2 : -1]
        
        # Проверяем полеis_valid = validate_field(mode, field_value)
        
        if is_valid:
            user.append(field_value)
        
        mode += 1
        
        # Если анкета полностью обработана и валидна
        if mode == 6 and is_valid:
            new_count, user_result = process_user_data(user, target_name, count)
            if new_count > count:
                count = new_count
                result_content += user_result
            mode = 0
            user.clear()
    
    return count, result_content


def main():
    """Основная функция программы"""
    # Парсим аргументы
    args = parse_arguments()
    input_file = args.input_file
    target_name = args.name
    output_file = args.output_file
    
    # Читаем данные из файла
    try:
        data = read_input_file(input_file)
    except Exception as e:
        print(f"Ошибка: {e}")
        return
    
    count, result_content = process_ankets_data(data, target_name)

    try:
        write_output_file(output_file, result_content)
        print(f"Количество людей по имени {target_name} = {count}")
        print(f"Результаты сохранены в файл: {output_file}")
    except Exception as e:
        print(f"Ошибка при сохранении результатов: {e}")

if __name__ == "__main__":
    main()