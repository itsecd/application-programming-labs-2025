import re
from collections import Counter
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
    try:
        content = read_file_content('data.txt')
        codes = extract_operator_codes(content)
        result = find_most_common_code(codes)
        
        if result:
            code, count = result
            print(f"Самый частый код оператора: {code}")
            print(f"Повторений: {count}")
        else:
            print("Коды операторов не найдены")
            
    except FileNotFoundError as e:
        print(f"Ошибка: {e}")
    except IOError as e:
        print(f"Ошибка ввода-вывода: {e}")
    except Exception as e:
        print(f"Неожиданная ошибка: {e}")


if __name__ == "__main__":
    main()