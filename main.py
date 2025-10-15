import argparse
import re

parser = argparse.ArgumentParser()
parser.add_argument('file_name', type=str)
args = parser.parse_args()
print(f"The name of the file is: {args.file_name}")


with open(args.file_name, "r", encoding="utf-8") as file:
    text = file.read()
