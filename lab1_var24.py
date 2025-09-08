import re
import argparse

def read_file(filename: str) -> str:
    """
    читаю содержимое файла
    """
    with open(filename,'r', encoding="utf-8") as filename:
        data = filename.read()

