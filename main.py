import re

def main(filename: str) -> None:
    """Основная логика программы"""
    pattern = r"@\w+.\w+"

    with open(f"{filename}", mode="r", encoding="utf8") as inp:
        domains = re.findall(pattern, inp.read())
    print(domains)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", type=str, help="путь до файла с данными")
    args = parser.parse_args()

    main(args.file)
