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


def load_image(image_path: str) -> np.ndarray:
    """
    Загрузка изображения из файла.
    """
    img = cv2.imread(image_path)
    if img is None:
        raise ValueError(f"Не удалось загрузить изображение: {image_path}")
    return img


def convert_and_binarize(img: np.ndarray, threshold: int) -> np.ndarray:
    """
    Преобразование изображения в оттенки серого и применение бинаризации.
    """
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, binary_img = cv2.threshold(gray_img, threshold, 255, cv2.THRESH_BINARY)
    return binary_img


def main() -> None:
    """
    Основная функция программы.
    """
    args = parse_arguments()
    
    try:
        validate_arguments(args.input, args.threshold)

        original_img = load_image(args.input)
        print(f"Изображение загружено: {args.input}")
        
        height, width, channels = original_img.shape
        print(f"Размер: {width}x{height}, Каналы: {channels}")
        
        binary_img = convert_and_binarize(original_img, args.threshold)
        print("Изображение преобразовано в бинарное")
        
    except Exception as e:
        print(f"Ошибка: {e}")


if __name__ == "__main__":
    main()