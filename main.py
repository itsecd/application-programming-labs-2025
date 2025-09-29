#Найдите все женские имена, начинающиеся с буквы А.
#Выведите их количество на экран и сохраните анкеты в новый файл.
import re 
import argparse

def is_name_correct(name: str)->bool:
    """
    Имя должно начинаться на заглавную А и состоять только из букв.
    """
    return re.fullmatch(r'А[а-яё]*', name) is not None

def is_female(gender: str)->bool:
    """
    Пол женский
    """
    return re.fullmatch(r'(Ж|ж|Женский|женский)', gender) is not None

def extract_value(line: str) -> str:
    """
    Извлекает значение после ':'.
    """
    return line.split(':', 1)[1].strip()

def form_is_correct(form:list[str])->bool:
    """
    Проверяет анкету на соответствие условию.
    """  
    name=extract_value(form[1])
    gender=extract_value(form[2])
    return is_name_correct(name) and is_female(gender)

def read_forms(filename:str)->list[list[str]]:
    """
    Читает файл и возвращает список анкет по 6 строк, пропуская номера и пустые строки
    """
    with open(filename,encoding="utf-8") as f:
         lines = [line.strip() for line in f if line.strip() and ':' in line]
    return [lines[i:i+6] for i in range(0, len(lines), 6)]

def save_forms(forms: list[list[str]], path: str = "filtered_forms.txt") -> None:
    """
    Сохраняет анкеты в файл.
    """
    with open(path, "w", encoding="utf-8") as f:
        for a in forms:
            f.write("\n".join(a) + "\n\n")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("filename")
    args = parser.parse_args()

    forms = read_forms(args.filename)
    correct = [a for a in forms if form_is_correct(a)]

    print(len(correct))
    save_forms(correct)

if __name__ == "__main__":
    main()