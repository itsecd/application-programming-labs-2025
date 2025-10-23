import argparse
from parser import Parser

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", required=True, help="path/to/file")
    args = parser.parse_args()

    processor = Parser(args.file)
    processor.parse()
    processor.save()

if __name__ == "__main__":
    main()

