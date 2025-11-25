import argparse

def parse_args() -> argparse.Namespace:
    """
    Разбор аргументов командной строки
    :return: аргументы командной строки
    """

    p = argparse.ArgumentParser(description="Сделать изображение полутоновым")

    p.add_argument("-i",
                   "--input",
                   required=True,
                   help="Путь к исходному изображению")

    p.add_argument("-o",
                   "--output",
                   default="Save_Result",
                   help="Путь для сохранения результата")

    return p.parse_args()