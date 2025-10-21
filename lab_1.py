#!/usr/bin/env python3

import re
import argparse


def read_file(filename: str) -> str | None:
    try:
        with open(filename, "r") as file:
            return file.read()
    except FileNotFoundError:
        print("File not found")


def write_file(filename: str, data: list[str]):
    with open(filename, "w+", encoding='utf-8') as file:
        for i, dat in enumerate(data, 1):
            file.write(f"{i})\n{dat}\n\n")

def args_parse() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="Data parser", description="Parsing data from file"
    )
    parser.add_argument("-f", "--file", type=str, help="Parse file")
    parser.add_argument("-o", "--output", type=str, help="Output file")
    return parser.parse_args()

def parse_data(data: str) -> list[str]:
    parts = [p.strip() for p in re.split(r'\n\d+\)\s*', data) if p.strip()]
    
    questionnaires = []
    
    for part in parts:
        last_name_match = re.search(r'Фамилия:\s*([^\n]+)', part)
        first_name_match = re.search(r'Имя:\s*([^\n]+)', part)
        
        if last_name_match and first_name_match:
            last_name = last_name_match.group(1).strip()
            first_name = first_name_match.group(1).strip()
            
            questionnaires.append({
                'last_name': last_name,
                'first_name': first_name,
                'text': part
            })
    
    sorted_questionnaires = sorted(questionnaires, 
                                 key=lambda x: (x['last_name'].lower(), 
                                              x['first_name'].lower()))
    
    return [q['text'] for q in sorted_questionnaires]

def main():
    args = args_parse()
    
    if not args.file:
        print("Please specify input file with -f option")
        return
    
    data = read_file(args.file)
    if not data:
        return
    
    parsed_data = parse_data(data)
    
    if args.output:
        write_file(args.output, parsed_data)
        print(f"Sorted data written to {args.output}")
    else:
        for i, dat in enumerate(parsed_data, 1):
            print(f"{i})\n{dat}\n")

if __name__ == "__main__":
    main()