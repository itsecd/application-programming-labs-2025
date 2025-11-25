import re
import argparse

def read_data(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        return file.read()

def extract_valid_names(data):
    lines = data.split('\n')
    names_list = []
    
    # Ищем пары "Фамилия: бла бла" и "Имя: бла бла"
    for i in range(len(lines)):
        line = lines[i].strip()
        
        if line.startswith('Фамилия: '):
            surname = line.replace('Фамилия: ', '').strip()
            
            if i + 1 < len(lines):
                name_line = lines[i + 1].strip()
                if name_line.startswith('Имя: '):
                    name = name_line.replace('Имя: ', '').strip()
                    
                    if re.match(r'^[А-ЯЁ][а-яё]*$', surname) and re.match(r'^[А-ЯЁ][а-яё]*$', name):
                        formatted = f"{surname} {name[0]}."
                        names_list.append(formatted)
    
    return sorted(names_list)

def save_to_file(names, filename):
    with open(filename, 'w', encoding='utf-8') as file:
        for name in names:
            file.write(name + '\n')

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', type=str, help='Название файла с данными')
    args = parser.parse_args()
    
    try:
        data = read_data(args.filename)
        
        # Извлекаем и форматируем имена
        names = extract_valid_names(data)
       
        save_to_file(names, 'sorted_names.txt')
        
        print("Результат:")
        for name in names:
            print(name)
            
    except FileNotFoundError:
        print(f"Ошибка: файл {args.filename} не найден")
    except Exception as e:
        print(f"Произошла ошибка: {e}")

if __name__ == "__main__":
    main()