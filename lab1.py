import argparse
from collections import Counter
import re
from typing import List, Tuple, Union


def read_file_content(filename: str) -> str:
    """
    Чтение содержимого файла.
    :param filename: имя файла для чтения
    :return: содержимое файла
    """
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"Файл '{filename}' не найден")
    except IOError as e:
        raise IOError(f"Ошибка чтения файла: {e}")


def extract_operator_codes(content: str) -> List[str]:
    """
    Извлечение кодов операторов из текста.
    :param content: текст для анализа
    :return: список найденных кодов операторов
    """
    pattern = r'[+78][\s\(]*(\d{3})'
    return re.findall(pattern, content)


def find_most_common_code(codes: List[str]) -> Union[Tuple[str, int], None]:
    """
    Поиск самого часто встречающегося кода оператора.
    :param codes: список кодов операторов
    :return: кортеж (код, количество повторений) или None если список пуст
    """
    if not codes:
        return None
    
    code_counter = Counter(codes)
    return code_counter.most_common(1)[0]


def main() -> None:

    parser = argparse.ArgumentParser(description='Анализ кодов операторов')
    parser.add_argument("input_file", type=str, help="Файл для чтения данных")
    parser.add_argument("output_file", type=str, help="Файл для записи результата")
    args = parser.parse_args()
    
    try:
        content = read_file_content(args.input_file)
        codes = extract_operator_codes(content)
        result = find_most_common_code(codes)
        
        if result:
            code, count = result
            print(f"Самый частый код оператора: {code}")
            print(f"Повторений: {count}")
         
            with open(args.output_file, 'w', encoding='utf-8') as f:
                f.write(f"Самый частый код оператора: {code}\n")
                f.write(f"Повторений: {count}\n")
        else:
            print("Коды операторов не найдены")
            with open(args.output_file, 'w', encoding='utf-8') as f:
                f.write("Коды операторов не найдены\n")
            
    except FileNotFoundError as e:
        print(f"Ошибка: {e}")
    except IOError as e:
        print(f"Ошибка ввода-вывода: {e}")
    except Exception as e:
        print(f"Неожиданная ошибка: {e}")


if __name__ == "__main__":
    main()