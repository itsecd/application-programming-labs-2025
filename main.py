import argparse
import re

def is_valid_email(email):
    pattern = r'[A-Za-z0-9._%+-]{1,64}@(gmail\.com|mail\.ru|yandex\.ru)'
    match = re.search(pattern, email)
    return bool(match)



def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('file_name', type=str)
    args = parser.parse_args()
    print(f"The name of the file is: {args.file_name}")

    with open(args.file_name, "r", encoding="utf-8") as file:
        text = file.read()

    records = re.split(r'\n\d+\)\n', text)
    
    result = []
    surname = None
    email = None
    
    for record in records:
        dataset = record.split('\n')
        surname = None
        email = None

        for data in dataset:
            if re.match(r'\s*Фамилия:', data):
                surname = data.split(r': ', 1)[1]

            elif re.match(r'\s*Номер телефона или email:', data):
                if is_valid_email(data):
                    email = data.split(r': ', 1)[1]
            
        if surname and email:
            result.append(f'{surname}: {email}')

    with open("result.txt", "w", encoding="utf-8") as file:
        for person in result:
            file.write(person + '\n')
        

if __name__ == "__main__":
    main()

''' что у нас там по порядку:
1. Открыть файл
2. Считать с него данные
3. Выбрать только то, что содержит Фамилия/Номер телефона
4. Отделить людей у которых номера телефона, а не почта
5. Проверить правильность написания почты и фамилии
6. Как-то объединить эти два показателя
7. Переместить данные в отдельную папку
8. Profit
'''