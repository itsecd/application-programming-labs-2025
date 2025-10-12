import re

def read_file(path: str) -> str:
    """
    Read file and return it's content
    """
    try:
        with open(path, 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError as err:
        raise FileNotFoundError(err)

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
        #TODO add func to read path from args
        path_file = "data.txt"
        data = read_file(path_file)
        candidates = split_candidates(data)
        fulfilling_candidates = find_candidates_by_phone_number(candidates, "927")
        for item in fulfilling_candidates:
            print(item)
        print(f"Number of fulfilling candidates: {len(fulfilling_candidates)}")
        #TODO add func to save fulfilling_candidates to file
    except Exception as err:
        print(f"Error while working with file: {err}")

if __name__ == "__main__":
    main()