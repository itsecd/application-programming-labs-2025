import argparse
import collections
import re




def read_from_file(filename):
    """Читает данные из файла и возвращает список строк."""
    with open(filename, mode="r", encoding="utf8") as f:
        return f.readlines()


def process_data(data):
    """
    Обрабатывает данные и подсчитывает коды операторов.
    Возвращает Counter с количеством вхождений каждого кода.
    """
    # Регулярное выражение для поиска валидных телефонных номеров по заданию
    PHONE_NUMBER_PATTERN = re.compile(
        r'(?:8|\+7)[\s\(]*(?P<code>\d{3})[\s\)]*\d{3}[\s\-]*\d{2}[\s\-]*\d{2}'
    )
    
    codes = collections.Counter()
    
    for string in data:
        # Ищем все телефонные номера в строке
        matches = PHONE_NUMBER_PATTERN.findall(string)
        for code in matches:
            codes[code] += 1
            
    return codes


def main():
    """Основная функция программы, которая управляет всем процессом выполнения.
    
    Выполняет следующие шаги:
    1. Парсит аргументы командной строки
    2. Читает данные из указанного файла
    3. Обрабатывает данные для поиска кодов операторов
    4. Выводит результаты анализа на экран
    5. Обрабатывает возможные ошибки выполнения
    
    Workflow:
        аргументы командной строки → чтение файла → обработка данных → вывод результатов"""
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", help="файл ввода", type=str, required=True)
    args = parser.parse_args()

    try:
        data = read_from_file(args.file)
        codes = process_data(data)
        
        if codes:
            # Находим самый частый код и все коды с количеством
            most_common_code, count = codes.most_common(1)[0]
            print(f"Самый частый код оператора: {most_common_code}")
            print(f"Количество повторений: {count}")
            
            # Дополнительно: выводим всю статистику для проверки
            print("\nПолная статистика кодов операторов:")
            for code, count in codes.most_common():
                print(f"Код {code}: {count} раз")
        else:
            print("Телефонные номера не найдены")
            
    except FileNotFoundError:
        print(f'Файл не найден: "{args.file}"')
    except Exception as e:
        print(f'Произошла ошибка: "{e}"')


if __name__ == "__main__":
    main()