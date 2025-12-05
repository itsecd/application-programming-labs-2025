import os

def read_file(path: str) -> str:
    ''' Читает файл и возвращает строку.'''
    try:
        with open(path, "r", encoding='utf-8') as file:
            lines = file.readlines()
            return [line.strip() for line in lines]
    except FileNotFoundError:
        print(f"Файл {path} не найден")
        return None
    except Exception as e:
        print(f"Ошибка чтения файла: {e}")
        return None


def write_processed_file(original_path: str, processed_lines: str, output_path: str = None ) -> bool:
    ''' Записывает обработанные данные в новый файл.''' 
    try:
        if output_path is None:
            directory = os.path.dirname(original_path)
            new_file_path = os.path.join(directory, 'data_processed.txt')
        
        os.makedirs(os.path.dirname(output_path), exist_ok=True)


        with open(output_path, 'w', encoding='utf-8') as new_file:
            for line in processed_lines:
                new_file.write(line + '\n')
        
        print(f"Файл успешно создан: {new_file_path}")
        return True
        
    except Exception as e:
        print(f"Ошибка при создании файла: {e}")
        return False