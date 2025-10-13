import re
import argparse

def parse_arguments() -> argparse.Namespace:
    """
    Adds and parses command-line arguments
    """
    parser = argparse.ArgumentParser(description="Search candidates by phone code")
    parser.add_argument('filename', help='File to search in')
    parser.add_argument('--output', '-o', help='File to save in search result')
    return parser.parse_args()

def read_file(path: str) -> str:
    """
    Read file and return it's content
    """
    try:
        with open(path, 'r', encoding='utf-8') as file:
            return file.read()
    except IOError as err:
        raise IOError(f"Wasn't able to read file at {path}: {err}")

def write_file(path: str, data: list[str]) -> None:
    """
    Write data in file
    """
    try:
        with open(path, 'w', encoding='utf-8') as file:
            file.write('\n\n'.join(data))
    except IOError as err:
        raise IOError(f"Wasn't able to write file at {path}: {err}")

def split_candidates(data: str) -> list[str]:
    """
    Split data to list of candidates
    """
    candidates = re.split(r'\n{2}', data)
    return candidates

def find_candidates_by_phone_number(candidates: list[str], code: str) -> list[str]:
    """
    Find candidates with matching phone code
    :param candidates: list of candidates
    :param code: phone code
    :return: list of fulfilling candidates
    """
    found_candidates = []
    #TODO add checking for valid forms of phone number
    pattern = f'{code}'

    for candidate in candidates:
        if re.search(pattern, candidate):
            found_candidates.append(candidate)

    return found_candidates

    #var7: Найдите всех людей, чьи телефоны имеют код города 927. Выведите их количество на экран и сохраните их анкеты в новый файл.

def main() -> None:
    """
    Main function
    """
    try:
        args = parse_arguments()
        data = read_file(args.filename)
        candidates = split_candidates(data)
        fulfilling_candidates = find_candidates_by_phone_number(candidates, "927")
        if fulfilling_candidates:
            for item in fulfilling_candidates:
                print(item)
            print(f"Number of fulfilling candidates: {len(fulfilling_candidates)}")
            if args.output:
                write_file(args.output, fulfilling_candidates)
                print(f"Successfully write output to: {args.output}")
        else:
            print("No fulfilling candidates!")
    except Exception as err:
        print(f"Error while working with file: {err}")

if __name__ == "__main__":
    main()