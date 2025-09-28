import re
import argparse


def parse_console () -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--read_file", type=str, help="Чтение файла из консоли")
    parser.add_argument("--write_file", type=str, helr="Запись нового файла")
    args = parser.parse_args()
    return args


def correct_numbers(text: str) -> list:
    profiles=re.split(r'\n(?=\d+\)\s*\n)', text)
    pattern= r'(?:\+7|8)[\s\-]?\(?\d{3}\)?[\s\-]?\d{3}[\s\-]?\d{2}[\s\-]?\d{2}'
    valid_profiles = []
    for profile in profiles:
        if re.search(pattern, profile):
            valid_profiles.append(profile)
    return valid_profiles
