import argparse
import matplotlib.pyplot as plt
import random
import cv2
import os
import numpy as np


def parse_arguments():
    """Парсинг аргументов командной строки."""
    parser = argparse.ArgumentParser(description='Создание паззла из изображения')
    parser.add_argument(
        '--input_image',
        required=True,
        help='Путь к исходному изображению'
    )
    parser.add_argument(
        '--output_dir',
        required=True,
        help='Папка для сохранения результатов'
    )
    return parser.parse_args()


def load_image(image_path):
    """
    Загрузка изображения.

    Args:
        image_path (str): Путь к изображению

    Returns:
        numpy.ndarray: Загруженное изображение
    """
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError(f"Не удалось загрузить изображение '{image_path}'")

    return image


def create_puzzle(image, rows, cols):
    """
    Создает паззл из изображения.

    Args:
        image (numpy.ndarray): Исходное изображение
        rows (int): Количество строк для разделения
        cols (int): Количество столбцов для разделения

    Returns:
        numpy.ndarray: Изображение-паззл
    """
    height, width = image.shape[:2]
    part_height = height // rows
    part_width = width // cols
    pieces = []
    for i in range(rows):
        for j in range(cols):
            piece = image[
                i * part_height:(i + 1) * part_height,
                j * part_width:(j + 1) * part_width
            ]
            pieces.append(piece)
    random.shuffle(pieces)
    puzzle = np.zeros((height, width, 3), dtype=np.uint8)
    piece_index = 0
    for i in range(rows):
        for j in range(cols):
            puzzle[
                i * part_height:(i + 1) * part_height,
                j * part_width:(j + 1) * part_width
            ] = pieces[piece_index]
            piece_index += 1

    return puzzle


def save_image(image, output_dir, filename):
    """
    Сохраняет изображение в указанную директорию.

    Args:
        image (numpy.ndarray): Изображение для сохранения
        output_dir (str): Директория для сохранения
        filename (str): Имя файла

    """
    if not os.path.exists(output_dir):
        try:
            os.makedirs(output_dir)
            print(f"Создана директория: {output_dir}")
        except OSError as e:
            raise OSError(f"Не удалось создать директорию '{output_dir}': {e}")

    output_path = os.path.join(output_dir, filename)

    try:
        success = cv2.imwrite(output_path, image)
        if not success:
            raise OSError(f"Не удалось сохранить изображение '{output_path}'")
        print(f"Изображение сохранено: {output_path}")
    except Exception as e:
        raise OSError(f"Ошибка при сохранении '{output_path}': {e}")


def display_images(original_image, puzzle_image):
    """
    Отображает оригинальное изображение и паззл.

    Args:
        original_image (numpy.ndarray): Оригинальное изображение
        puzzle_image (numpy.ndarray): Изображение-паззл
    """
    original_rgb = cv2.cvtColor(original_image, cv2.COLOR_BGR2RGB)
    puzzle_rgb = cv2.cvtColor(puzzle_image, cv2.COLOR_BGR2RGB)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))
    ax1.imshow(original_rgb)
    ax1.set_title('Оригинальное изображение')
    ax1.axis('off')
    ax2.imshow(puzzle_rgb)
    ax2.set_title('Пазл')
    ax2.axis('off')
    plt.tight_layout()
    plt.show()


def print_image_info(image):
    """
    Выводит информацию об изображении.

    Args:
        image (numpy.ndarray): Изображение для анализа
    """
    height, width, channels = image.shape
    print(f"Размер изображения: {width} x {height} пикселей")
    print(f"Количество каналов: {channels}")


def main():
    """Основная функция программы."""
    try:
        args = parse_arguments()
        original_image = load_image(args.input_image)
        print_image_info(original_image)
        print("На сколько частей разбить изображение")
        rows = int(input())
        cols = int(input())
        puzzle_image = create_puzzle(original_image, rows, cols)
        save_image(puzzle_image, args.output_dir, 'puzzle.jpg')
        display_images(original_image, puzzle_image)
    except FileNotFoundError as e:
        print(f"❌ Ошибка: {e}")
    except ValueError as e:
        print(f"❌ Ошибка: {e}")
    except OSError as e:
        print(f"❌ Ошибка ввода-вывода: {e}")
    except Exception as e:
        print(f"❌ Неожиданная ошибка: {e}")


if __name__ == "__main__":
    main()