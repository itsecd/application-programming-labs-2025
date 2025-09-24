import re
import argparse


def read_file(filename: str) -> str:
    """Эта функция возвращает текст как одну большую строку"""

    try:
        with open(filename, "r", encoding="utf-8") as file:
            return file.read()
    except:
        raise Exception("Ошибка при открытии файла")


def write_file(filename: str, data: list[str]) -> None:
    """Эта фунция выполняет запись найденных анкет в файл"""

    with open(filename, "w", encoding="utf-8") as file:
        count = 1

        for item in data:
            file.write(f"{count})\n{item}")
            count += 1


def args_parse() -> tuple[str, str]:
    """Эта функция парсит аргументы из консоли"""
    
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", help="Input file")
    parser.add_argument("-o", "--output", help="Output file")
    args = parser.parse_args()

    if args.output is not None:
        return (args.input, args.output)
    else:
        raise Exception("The name of output file can't be None")


def forms_parse(text: str) -> list[str]:
    """
    Эта функция разделяет текст по заданному паттерну(по номеру анкет).
    Затем происходит парсинг анкет, которые удовлетворяют условию задания.
    """
    pattern = r'\d+\)\n'
    forms = list(filter(None, re.split(pattern, text)))

    result = []

    for item in forms:
        temp_list = list(filter(None, item.split("\n")))
        pattern = r'Фамилия: [А-Я][а-я]*ов(а)?$'
        
        for line in temp_list:
            if re.match(pattern, line.strip()):
                result.append(item)
                break        

    return result 


def main() -> None:
    file, output = args_parse()
    text = read_file(file)
    result = forms_parse(text)
    print(f"Найдено {len(result)} подходящих анкет")
    write_file(output, result)


if __name__ == "__main__":
    main()