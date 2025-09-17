import re

def main(filename: str) -> None:
    """Основная логика программы"""
    pattern = r"@\w+.\w+"

    with open(f"{filename}", mode="r", encoding="utf8") as inp:
        domains = list(map(lambda x: x[1::], re.findall(pattern, inp.read()))) 
        # чтобы избавиться от лишней '@' в начале ^
    
    results = dict.fromkeys(domains, 0)
    for domain in domains:
        results[domain] += 1

    with open("output.txt", mode="w", encoding="utf8") as out:
        for dom, num in sorted(results.items(), key=lambda x: x[1], reverse=True):
            out.write(f"{dom}: {num}\n")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", type=str, help="путь до файла с данными")
    args = parser.parse_args()

    try:
        main(args.file)
    except Exception as e:
        print(e)
