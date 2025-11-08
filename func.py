import argparse
import re


def get_args():
    filenames = []
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file", type=str)
    parser.add_argument("output_file", type=str)
    args = parser.parse_args()
    filenames.append(args.input_file)
    filenames.append(args.output_file)
    return filenames


def read_file(filename: str) -> str:
    try:
        with open(filename, "r", encoding="utf-8") as file:
            return file.read()
    except FileNotFoundError:
        return ""


def is_valid_email(contact: str) -> bool:
    pattern = r'^[a-zA-Z0-9._%+-]{1,64}@(gmail\.com|mail\.ru|yandex\.ru)$'
    return bool(re.match(pattern, contact))


def write_emails(file, emails_list):
    for email in emails_list:
        file.write(email + "\n")