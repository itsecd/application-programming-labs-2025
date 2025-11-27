import os
import argparse
from image_utils import (
    load_image,
    get_image_size,
    convert_to_pixel_art,
    display_images,
    save_image,
)


def parse_arguments() -> argparse.Namespace:
    """
    Парсит аргументы командной строки для преобразования в пиксель-арт

    Returns:
        argparse.Namespace: Объект с распарсенными аргументами
    """
    parser = argparse.ArgumentParser(
        description="Преобразование изображения в пиксель-арт"
    )
    parser.add_argument("input_path", type=str, help="Путь к исходному изображению")
    parser.add_argument("output_path", type=str, help="Путь для сохранения результата")
    parser.add_argument(
        "--pixel_size", type=int, default=10, help="Размер пикселя (по умолчанию: 10)"
    )

    return parser.parse_args()


def main() -> None:
    """Основная функция"""
    args: argparse.Namespace = parse_arguments()

    if not os.path.exists(args.input_path):
        print(f"Ошибка: файл {args.input_path} не существует")
        return

    print("Загрузка изображения")
    original_image = load_image(args.input_path)

    width: int
    height: int
    width, height = get_image_size(original_image)
    print(f"Размер изображения: {width}x{height} пикселей")

    print(f"Преобразование в пиксель-арт (размер пикселя: {args.pixel_size})")
    pixel_art_image = convert_to_pixel_art(original_image, args.pixel_size)

    save_image(pixel_art_image, args.output_path)

    print("Отображение результатов...")
    display_images(original_image, pixel_art_image)

    print("Готово!")


if __name__ == "__main__":
    main()
