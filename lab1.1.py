import argparse
import re

def openfile()->list[str]:
    """
    Функция для чтения из файла
    С помощью argarce мы передаем имя файла как аргумент командной строки
    Далее делаем проверку и закрываем файл
    """
    parser = argparse.ArgumentParser()  
    parser.add_argument('file', type=str, help='file')  
    args = parser.parse_args()
    try:
        file = open(args.file, 'r', encoding='utf-8')
    except FileNotFoundError as exs:
        print(f"Error: {exs}")
        return None
    
    text = file.read()
    file.close()
    return text
def get_full_records_by_name(name:str)->list[str]:
    """
    Функция для проверки анкет по имени
    Сначала передаем имя которое ввел пользователь 'name'
    далее создаем список в котором будут храниться нужные анкеты
    проводим проверку с анкетами и функция возвращает список анкет
    """
    text=openfile()
    if text is None:
        return []
    blocks = text.split('\n\n')
    records = []
    for block in blocks:
      cleaned_block = block.strip()
      if cleaned_block:
        records.append(cleaned_block)
    found_records=[]
    for record in records:
        
        lines = record.splitlines()
        for line in lines:
            if line.startswith('Имя:'):
                parts = line.split(':', 1)
                record_name = parts[1]
                record_name=record_name.strip()
                record_name = record_name.lower()
                if re.search(name, record_name) :
                    found_records.append(record)
                    break
    return found_records 

def ritefile(found_records:list[str]) -> None:
    """
    функция для записи в файл
    """
    try:
      file = open('data1.txt', 'w', encoding='utf-8')
    except FileNotFoundError as exs:
        print(f"Error: {exs}")
        return None
        
    for exit_file in found_records:
        file.write(exit_file + '\n\n')
    return None