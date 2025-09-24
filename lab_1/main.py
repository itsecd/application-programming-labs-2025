import re
import argparse

def read_file(path: str) -> list[str]:
    try:
        with open(path, "r", encoding="utf-8") as file:
            pattern = r'\d+[)][\n*]'
            text = list(filter(None, re.split(pattern, file.read())))

            return text
    except:
        raise Exception("Ошибка при открытии файла")


def main() -> None:
    
    

if __name__ == "__main__":
    main()