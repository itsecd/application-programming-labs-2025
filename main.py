import re

def main(filename: str) -> None:
    """Основная логика программы"""
    EMAIL_PATTERN = re.compile(r"[a-zA-z0-9]+@(?P<domain>[a-z]+[.][a-z]+)")

    domains = dict()
    with open(f"{filename}", mode="r", encoding="utf8") as inp:
        for line in inp.readlines():
            match = EMAIL_PATTERN.search(line)
            if match:
                domain = match.group('domain')
                if domain not in domains:
                    domains[domain] = 0
                else:
                    domains[domain] += 1

    with open("output.txt", mode="w", encoding="utf8") as out:
        for dom, num in sorted(domains.items(), key=lambda x: x[1], reverse=True):
            out.write(f"{dom}: {num}\n")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", type=str, help="путь до файла с данными")
    args = parser.parse_args()

    try:
       main(args.file)
    except FileNotFoundError as e:
        print(f'Ошибка, не найден файл: "{e.filename}"')
    except PermissionError as e:
         print(f"Недостаточно прав для совершения операции: {e}")
