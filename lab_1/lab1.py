"""
Var_12 Определите, какой код оператора чаще всего 
встречается в телефонных номерах. Выведите
на экран код и количество его повторений.
"""


import argparse
import re
from typing import List, Dict, Tuple, Optional


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('name', type=str, help='your name')
    args = parser.parse_args()
if __name__ == "__main__":
    main()