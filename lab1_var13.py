import re
import argparse

def parse_console () -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--path_file", type=str, help="������ ����� �� �������")
    args = parser.parse_args()
    return args