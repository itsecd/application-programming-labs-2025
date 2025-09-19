import re
import argparse
from collections import Counter

def student_name():
    print("Студент: Илья Магров Сергеевич\nГруппа: 6214-100503D\nВариант: 12\n")

def extract_phone_numbers(text):
    """Извлечение телефонных номеров из текста"""
    # Регулярное выражение для поиска телефонных номеров
    phone_pattern = r'(?:\+7|8)[\s\(\-]*(\d{3})[\s\)\-]*\d{3}[\s\-]*\d{2}[\s\-]*\d{2}'
    return re.findall(phone_pattern, text)

def main():
    # Настройка аргументов командной строки
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
    
    # Парсинг аргументов
    args = parser.parse_args()

    student_name()
    
    try:
        # Читаем файл
        with open(args.filename, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Извлекаем телефонные номера и коды операторов
        phone_codes = extract_phone_numbers(content)
        
        if not phone_codes:
            print("Телефонные номера не найдены в файле")
            return
        
        # Считаем частоту кодов операторов
        code_counter = Counter(phone_codes)
        total_phones = len(phone_codes)
        
        # Находим самый частый код и его количество
        most_common_code, count = code_counter.most_common(1)[0]
        
        print(f"Файл: {args.filename}")
        print(f"Всего телефонных номеров: {total_phones}")
        print(f"Уникальных кодов операторов: {len(code_counter)}")
        print(f"\nСамый частый код оператора: {most_common_code}")
        print(f"Количество повторений: {count}")
        
        # Выводим топ-N кодов
        top_n = min(args.top, len(code_counter))
        print(f"\nТоп-{top_n} кодов операторов:")
        for i, (code, cnt) in enumerate(code_counter.most_common(top_n), 1):
            print(f"{i:2d}. Код {code}: {cnt:2d} раз(а)")
        
    except FileNotFoundError:
        print(f"Ошибка: файл '{args.filename}' не найден")
    except Exception as e:
        print(f"Произошла ошибка: {e}")

if __name__ == "__main__":
    main()
