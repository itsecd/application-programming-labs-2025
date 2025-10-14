import argparse
import collections
import re
from typing import List, Pattern, Tuple


def read_from_file(filename: str) -> List[str]:
    """Читает данные из файла и возвращает список строк."""
    with open(filename, mode="r", encoding="utf8") as f:
        return f.readlines()


def process_data(data: List[str]) -> collections.Counter:
    """
    Обрабатывает данные и подсчитывает коды операторов.
    Возвращает Counter с количеством вхождений каждого кода.
    """
    # Регулярное выражение для поиска валидных телефонных номеров 
    PHONE_NUMBER_PATTERN: Pattern = re.compile(
        r'(?:8|\+7)[\s\(]*(?P<code>\d{3})[\s\)]*\d{3}[\s\-]*\d{2}[\s\-]*\d{2}'
    )
    
    codes: collections.Counter = collections.Counter()
    
    for string in data:
        # поиск всех номеров в строке
        matches: List[str] = PHONE_NUMBER_PATTERN.findall(string)
        for code in matches:
            codes[code] += 1
            
    return codes


def main() -> None:
    """Основная функция программы, которая управляет всем процессом выполнения.
    
    Выполняет следующие шаги:
    1. Парсит аргументы командной строки
    2. Читает данные из указанного файла
    3. Обрабатывает данные для поиска кодов операторов
    4. Выводит результаты анализа на экран
    5. Обрабатывает возможные ошибки выполнения
    
    Workflow:
        аргументы командной строки → чтение файла → обработка данных → вывод результатов
    """
    parser: argparse.ArgumentParser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", help="файл ввода", type=str, required=True)
    args: argparse.Namespace = parser.parse_args()

    try:
        data: List[str] = read_from_file(args.file)
        codes: collections.Counter = process_data(data)
        
        if codes:
            # ПОИСК САМОГО ЧАСТОГО КОДА и все коды с количеством
            most_common_code: Tuple[str, int] = codes.most_common(1)[0]
            code: str = most_common_code[0]
            count: int = most_common_code[1]
            
            print(f"Самый частый код оператора: {code}")
            print(f"Количество повторений: {count}")
            
            #  вывод всей статистики для проверки
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