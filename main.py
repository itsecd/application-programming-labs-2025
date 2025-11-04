import soundfile as sf
import matplotlib.pyplot as plt
from random import random

def main(file_path: str, output_path: str) -> None:
    """ 
    Основная логика программы 
    Args:
        file_path (str): Путь до обрабатываемого файла
        output_path (str): Путь для сохранения результата
    """

    data, samplerate = sf.read(file_path)
    print(f"Массив сэмплов: {data}")
    print(f"Частота дискретизации: {samplerate}")

    # sf.write(output_path, data, samplerate)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", type=str, help="Аудиофайл для обработки")
    parser.add_argument("-o", "--out", type=str, help="Путь для сохранения результата", default="res.mp3")
    args = parser.parse_args()

    try:
        main(args.file, args.out)
    except FileNotFoundError as e:
        print(f'Ошибка, не найден файл: "{e.filename}"')
    except PermissionError as e:
        print(f"Недостаточно прав для совершения операции: {e}")