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
    count = 1
    with open(filename, "w+") as file:
        for d in data:
            file.write(f"{count})\n" + d + "\n")