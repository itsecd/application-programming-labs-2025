import argparse
import cv2
import numpy as np
import matplotlib.pyplot as plt


def args_parse() -> argparse.Namespace:
    """Данная функция получает аргументы(input_file_path, result_file_path)"""
    parser = argparse.ArgumentParser()

    parser.add_argument("-i", "--input_file", help="Путь к исходноому изображению")
    parser.add_argument("-r", "--result_file", help="Путь для сохранения обработанного изображения")

    args = parser.parse_args()

    
    if (args.input_file and args.result_file) is not None:
        return args
    else:
        raise Exception("Incorrectly passed arguments")


def main() -> None:
    arguments = args_parse()
    input_file = arguments.input_file
    result_file = arguments.result_file


if __name__ == "__main__":
    main()