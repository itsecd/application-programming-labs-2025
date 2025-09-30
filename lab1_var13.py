import argparse
import re


def parse_console () -> argparse.Namespace:
    """
 Парсер для аргументов в консоли

 -r_file Путь к файлу для чтения
 -W_file Путь к новому файлу с подходящими анкетами 
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("-r", "--r_file", type=str, help="Чтение файла из консоли")
    parser.add_argument("-w", "--w_file", type=str, help="Запись нового файла")
    args = parser.parse_args()
    return args


def correct_numbers(text: str) -> list:
    """
 Извлекает анкеты с корректными номерами телефонов
    """
    profiles=re.split(r'\n(?:\d+\)\s*\n)', text)
    pattern= r'(?:\+7|8)[\s]?\(?\d{3}\)?[\s]?\d{3}[\s\-]?\d{2}[\s\-]?\d{2}'
    correct_profiles = []
    for profile in profiles:
        if re.search(pattern, profile):
            correct_profiles.append(profile)
    return correct_profiles



def read_file(text: str) -> str:
    """
 Читает содержимое файла
    """
    with open(text, 'r', encoding = 'utf-8') as file:
        return file.read()



def write_file(new_text: str, profiles: list) -> None: 
    """
 Записывает найденные анкеты в новый файл
    """
    with open(new_text, 'w', encoding = 'utf-8') as file:
        for profile in profiles:
            file.write(profile + "\n\n")
           




def main() -> None:
    try:
        args = parse_console()
        text = read_file(args.r_file)
        correct_profiles = correct_numbers(text)
        write_file(args.w_file, correct_profiles)
        print(f'Успешно найденных анкет: {len(correct_profiles)}')
        print(f'Записаны в файл: {args.w_file}')

    except FileNotFoundError:
         print("Ошибка. Данный файл не найден")
    except Exception as e:
        print("Ошибка при чтении файла")

    
if __name__=="__main__":
    main()