'''
Функции для работы с файлом

'''
import os

def read_file(path: str) -> str:
    ''' 
    Читает файл и возвращает строку
    :path: путь к фалу
    '''
    try:
        with open(path, "r", encoding='utf-8') as file:
            lines = file.readlines()
            return [line.strip() for line in lines]
    except FileNotFoundError:
        print(f"Файл {path} не найден")
        return None
    except OSError as e:
        print(f"Ошибка чтения файла '{path}': {e}")
        return None

def write_processed_file(original_path: str, processed_lines: str, output_path: str = "") -> bool:
    """
    Записывает обработанные данные в новый файл.
    :original_path: путь к исходному файлу
    :processed_lines: список строк для записи
    :output_path: путь к выходному файлу (пустая строка для автосоздания)
    """
    try:
        new_file_path = output_path
        if not output_path:
            directory = os.path.dirname(original_path)
            if not directory:
                directory = "."
                new_file_path = os.path.join(directory, 'data_processed.txt')
        os.makedirs(os.path.dirname(new_file_path), exist_ok=True)
        with open(new_file_path+"\\data_pricessors.txt", 'w', encoding='utf-8') as new_file:
            for line in processed_lines:
                new_file.write(line + '\n')
        print(f"Файл успешно создан: {new_file_path}")
        return True
    except FileNotFoundError:
        print(f"Ошибка: директория не найдена для пути '{new_file_path}'")
        return False
    except OSError as e:
        print(f"Ошибка при записи файла '{new_file_path}': {e}")
    return False
