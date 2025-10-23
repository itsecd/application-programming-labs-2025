import argparse

def parser_t() -> tuple[str, str, str, int]:
    """
    Позволяет через консоль запускать код с аргументами
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('source', type=str,
                        help='Путь к файлу для работы с ним')
    parser.add_argument('output_file', type=str,
                        help='Путь для сохранения картинки')
    parser.add_argument('music', type=str,
                        help='Путь для сохранения музыки')
    parser.add_argument('alpha', type=int,
                        help='Число для ускорения')
    args = parser.parse_args()
    return args.source, args.output_file, args.music, args.alpha
