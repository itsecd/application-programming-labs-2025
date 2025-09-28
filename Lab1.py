import argparse
import re


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("input", help="input file path")
    parser.add_argument("output", help="output file path")
    args = parser.parse_args()
    return args

def read_file(name:str) -> str:
    with open(name, "r", encoding="utf-8") as file:
        return file.read()

def write_file(name:str, ovas:list[str]) -> None:
    with open(name, "w", encoding="utf-8") as file:
        file.write("\n\n".join(ovas))

def find_ovas(data:str) -> list[str]:
    people = re.split(r'\n\n', data)
    ovas = []
    for person in people:
        if re.search(r'Фамилия: \w+ова?\n', person):
            ovas.append(person)
    return ovas

def main() -> None:
    args = parse_arguments()
    data = read_file(args.input)
    ovas = find_ovas(data)

    print(len(ovas))
    write_file(args.output, ovas)

if __name__ == "__main__":
    main()