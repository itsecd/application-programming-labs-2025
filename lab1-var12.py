import re
import argparse
from collections import Counter

def student_name():
    """Вывод информации о студенте"""
    print("Студент: Илья Магров Сергеевич\nГруппа: 6214-100503D\nВариант: 12\n")

def extract_phone_numbers(text):
    """Извлечение телефонных номеров из текста"""
    phone_pattern = r'(?:\+7|8)[\s\(\-]*(\d{3})[\s\)\-]*\d{3}[\s\-]*\d{2}[\s\-]*\d{2}'
    return re.findall(phone_pattern, text)

def read_file(filename):
    """Чтение содержимого файла"""
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"Файл '{filename}' не найден")
    except Exception as e:
        raise Exception(f"Ошибка при чтении файла: {e}")

def analyze_phone_codes(phone_codes):
    """Анализ кодов операторов"""
    if not phone_codes:
        return None, 0, Counter()
    
    code_counter = Counter(phone_codes)
    total_phones = len(phone_codes)
    
    if code_counter:
        most_common_code, count = code_counter.most_common(1)[0]
        return most_common_code, count, code_counter
    else:
        return None, 0, code_counter

def display_results(filename, total_phones, unique_codes, most_common_code, count, code_counter, top_n):
    """Вывод результатов анализа"""
    print(f"Файл: {filename}")
    print(f"Всего телефонных номеров: {total_phones}")
    print(f"Уникальных кодов операторов: {unique_codes}")
    
    if most_common_code:
        print(f"\nСамый частый код оператора: {most_common_code}")
        print(f"Количество повторений: {count}")
        
        # Выводим топ-N кодов
        display_top = min(top_n, len(code_counter))
        print(f"\nТоп-{display_top} кодов операторов:")
        for i, (code, cnt) in enumerate(code_counter.most_common(display_top), 1):
            print(f"{i:2d}. Код {code}: {cnt:2d} раз(а)")

def process_file(filename, top_count=1):
    """Основная функция обработки файла"""
    content = read_file(filename)
    phone_codes = extract_phone_numbers(content)
    
    if not phone_codes:
        print("Телефонные номера не найдены в файле")
        return
    
    most_common_code, count, code_counter = analyze_phone_codes(phone_codes)
    
    display_results(
        filename=filename,
        total_phones=len(phone_codes),
        unique_codes=len(code_counter),
        most_common_code=most_common_code,
        count=count,
        code_counter=code_counter,
        top_n=top_count
    )

def main():
    """Главная функция программы"""
    parser = argparse.ArgumentParser(
        description='Анализ телефонных номеров: поиск самого частого кода оператора'
    )
    parser.add_argument(
        'filename',
        help='Путь к файлу с данными (например: data.txt)'
    )
    parser.add_argument(
        '-t', '--top',
        type=int,
        default=1,
        help='Количество топовых кодов для отображения (по умолчанию: 5)'
    )
    
    args = parser.parse_args()
    student_name()
    
    try:
        process_file(args.filename, args.top)
    except FileNotFoundError as e:
        print(f"Ошибка: {e}")
    except Exception as e:
        print(f"Произошла ошибка: {e}")

if __name__ == "__main__":
    main()
