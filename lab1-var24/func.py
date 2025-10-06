import re
import argparse

def get_args() -> str:
    """Parsing arguments in console"""
    parser = argparse.ArgumentParser() 
    parser.add_argument('filename', type=str, help='filename') 
    parser.add_argument('filename_result', type=str, help='filename_result') 

    args = parser.parse_args()
    if not (args.filename and args.filename_result):
        return None

    return args.filename, args.filename_result


def read_file(filename: str) -> str:
    """Reading file filename"""
    try:
        with open(filename, 'r', encoding = "utf-8") as file:
            return file.readlines()
    except FileNotFoundError:
        return None


def is_correct_date(date: str) -> bool:
    """Data correctness checking with same separator"""
    pattern = (
        r'(0?[1-9]|[12][0-9]|3[01])'
        r'([./-])'                   
        r'(0?[1-9]|1[0-2])'
        r'\2'                       
        r'((19\d{2})|(20(0\d|1\d|2[0-5])))'
    )
    return bool(re.fullmatch(pattern, date))


def parse_people(lines: list[str]) -> list[list[str, tuple[int, int, int]]]:
    """Parsing date: creating list of people with correct date"""
    text = ''.join(lines)  
    blocks = text.split('\n\n')
 
    people = []
    
    for block in blocks:
        surname_match = re.search(r'Фамилия:\s*(.+)', block)
        date_match = re.search(r'Дата рождения:\s*([^\n]+)', block)
        
        if not (surname_match and date_match):
            continue
        
        surname = surname_match.group(1).strip()
        date_str = date_match.group(1).strip()
            
        if not (is_correct_date(date_str)):
            continue

        for sep in ['.', '/', '-']:
            if sep in date_str:
                parts = date_str.split(sep)
                break
        else:
            continue

        if len(parts) != 3:
            continue
                
        day, month, year = parts
        day, month, year = int(day), int(month), int(year)
                
        people.append([surname, (year, month, day)])

    return people


def write_file(people: list[list[str, tuple[int, int, int]]], filename_result: str) -> None:
    """Writing list of people to filename_result"""
    try:
        with open(filename_result, 'w', encoding='utf-8') as file:
            for surname, (year, month, day) in people:
                file.write(f"{surname}: {day:02d}.{month:02d}.{year}\n")
    except IOError as error:
        print(f"Error writing to file {filename_result}: {error}")


def process_people(lines: list[str], filename_result: str) -> None:
    """Parsing date, checking data correctness, age sorting and writing to file"""
    people = parse_people(lines)   
    
    people.sort(key=lambda x: x[1])

    write_file(people, filename_result)
