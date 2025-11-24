import argparse
import os


def parse_arguments():
    """
    Парсинг аргументов командной строки.
    """

    parser = argparse.ArgumentParser(description='Преобразование изображения в бинарное')
    parser.add_argument('-i', '--input', type=str, required=True,
                       help='Путь к исходному изображению')
    parser.add_argument('-o', '--output', type=str, default='binary_result.jpg',
                       help='Путь для сохранения обработанного изображения')
    parser.add_argument('-th', '--threshold', type=int, default=127,
                       help='Порог для бинаризации (0-255)')
    return parser.parse_args()


def validate_arguments(input_path: str, threshold: int) -> None:
    """
    Проверка корректности аргументов командной строки.
    """
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Файл не найден: {input_path}")
    
    if not 0 <= threshold <= 255:
        raise ValueError("Порог должен быть в диапазоне от 0 до 255")
    

def main() -> None:

    args = parse_arguments()
    
    try:
        validate_arguments(args.input, args.threshold)
        print(f"Аргументы корректны: input={args.input}, output={args.output}, threshold={args.threshold}")
        
    except Exception as e:
        print(f"Ошибка: {e}")


if __name__ == "__main__":
    main()