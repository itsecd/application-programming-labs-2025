import re
import argparse


def parse_console () -> argparse.Namespace:
    """
 ������ ��� ���������� � �������
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("--read_file", type=str, help="������ ����� �� �������")
    parser.add_argument("--write_file", type=str, helr="������ ������ �����")
    args = parser.parse_args()
    return args


def correct_numbers(text: str) -> list:
    """
 ��������� ������ � ����������� �������� ���������
    """
    profiles=re.split(r'\n(?=\d+\)\s*\n)', text)
    pattern= r'(?:\+7|8)[\s\-]?\(?\d{3}\)?[\s\-]?\d{3}[\s\-]?\d{2}[\s\-]?\d{2}'
    correct_profiles = []
    for profile in profiles:
        if re.search(pattern, profile):
            correct_profiles.append(profile)
    return correct_profiles



def read_file(text: str) -> str:
    """
 ������ ���������� �����
    """
    try:
        with open(text, 'r', encoding = 'utf-8') as file:
            return file.read()
    except FileNotFoundError:
        print("������. ������ ���� �� ������")
        return ""



def write_file(text: str, profiles: list) -> None: 
    """
 ���������� ��������� ������ � ����� ����
    """
    try:
        with open(text, 'w', encoding = 'utf-8') as file:
            for profile in profiles:
                file.write(profile + "\n\n")
    except Exception as e:
        print("������ ��� ������ �����.")

