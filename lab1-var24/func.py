import re
import argparse

def get_args() -> str:
    """Parsing arguments in console"""
    parser = argparse.ArgumentParser() 
    parser.add_argument('filename', type=str, help='filename') 
    args = parser.parse_args()
    if args.filename is None:
        return None
    return args.filename


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


def process_people(lines: list[str], filename_result: str) -> None:
    """Parsing date, checking data correctness, age sorting and writing to file"""
    text = ''.join(lines)  
    blocks = text.split('\n\n')
    
    people = []
    
    for block in blocks:
        surname_match = re.search(r'Фамилия:\s*(.+)', block)
        date_match = re.search(r'Дата рождения:\s*([^\n]+)', block)
        
        if surname_match and date_match:
            surname = surname_match.group(1).strip()
            date_str = date_match.group(1).strip()
            
            if is_correct_date(date_str):
                sep = None
                for s in ['.', '/', '-']:
                    if s in date_str:
                        sep = s
                        break
                
                if sep is None:
                    continue  
                
                parts = date_str.split(sep)
                if len(parts) != 3:
                    continue 
                
                day, month, year = parts
                day, month, year = int(day), int(month), int(year)
                
                people.append([surname, (year, month, day)])
    
    people.sort(key=lambda x: x[1])
    
    try:
        with open(filename_result, 'w', encoding='utf-8') as file:
            for surname, (year, month, day) in people:
                file.write(f"{surname}: {day:02d}.{month:02d}.{year}\n")
    except IOError as error:
        print(f"Error writing to file {filename_result}: {error}")
