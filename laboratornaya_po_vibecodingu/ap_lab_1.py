import re
import argparse


def open_file(filename: str) -> str:
    """
    Функция читает файл и возвращает его содержимое в виде одной строки
    Если файл не существует, прокидывает ошибку
    """
    try:
        with open(filename, "r", encoding="utf-8") as file:
            data = file.read()
            return data
    except FileNotFoundError or EOFError as Open_File_Error:
        raise FileNotFoundError(f"Файл с таким именем ({filename}) не найден, увынск(")
        

def find_full_names(source_str: str) -> list:
    """
    Функция ищет все имена и фамилии в списке
    """
    full_names = re.findall(r'Фамилия:\s+\w+\nИмя:\s+\w+', source_str)
    return full_names


def find_correct_names(full_names: list[str]) -> list[str]:
    """
    Функция проверяет коррекность фамилии и имени и возвращает список с корректными значениями
    """
    res_names = []
    for full_name in full_names:
        temp = full_name.split("\n")
        name = temp[1]
        surname = temp[0]
        if name[5]==name[5].upper() and surname[9]==surname[9].upper():
            res_names.append(full_name)
    return res_names


def format_full_names(names: list[str]) -> list[str]:
    """
    Функция получает на вход список с именами и фамилиями и возвращает
    список с именами и фамилиями в формате "Фамилия И." 
    """
    res=[]
    for full_name in names:
        f_name=full_name.split("\n")
        formated_name = f_name[0][9:] + " " + f_name[1][5] + "."
        res.append(formated_name)
    return res


def write_full_names(filename: str, lst: list) -> None:
    """
    Функция записывает список в указанный файл
    """
    with open(filename, "w", encoding="utf-8") as file:
        if lst:
            if len(lst)>1:
                for i in range(len(lst)-1):
                    file.write(lst[i]+"\n")
            file.write(lst[len(lst)-1])


def parser_func() -> tuple[str, str] :
    """
    функция для ввода названий файлов ввода и вывода
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('input_file', type=str, help='Path to input file')
    parser.add_argument('output_file', type=str, help='Path to output file')

    args = parser.parse_args()
    return args.input_file, args.output_file


def main() -> None:
    """
    Главная функция, которая управляет работой программы
    """
    input_filename, output_filename = parser_func()
    try:
        lst_full_names = format_full_names(find_correct_names(find_full_names(open_file(input_filename))))
        write_full_names(output_filename, sorted(lst_full_names))
    except Exception as Open_File_Error:
        print(f"В процессе выполнения произошла ошибка: {Open_File_Error}")

if __name__=='__main__':
    main()
