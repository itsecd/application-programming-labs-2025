import argparse

from image_processor import ImageProcessor
from visualization import ImageVisualizer


def main():
    """Главная функция для обработки изображений через командной строки."""
    parser = argparse.ArgumentParser(
        description='Обработка изображений: смена каналов местами'
    )
    parser.add_argument(
        '--input', type=str, required=True,
        help='Путь к исходному изображению'
    )
    parser.add_argument(
        '--output', type=str, required=True,
        help='Путь для сохранения результата'
    )
    
    args = parser.parse_args()

    print("=== Обработка изображения ===")
    print(f"Входной файл: {args.input}")
    print(f"Выходной файл: {args.output}")

    try:
        processor = ImageProcessor()
        original_image, processed_image = processor.swap_channels(args.input)

        print(f"Размер изображения: {original_image.shape}")

        visualizer = ImageVisualizer()
        visualizer.show_comparison(original_image, processed_image, args.input)

        processor.save_image(processed_image, args.output)
        print(f"Результат сохранен в: {args.output}")

    except FileNotFoundError as e:
        print(f"Ошибка: {e}")
    except ValueError as e:
        print(f"Ошибка: {e}")
    except Exception as e:
        print(f"Неизвестная ошибка: {e}")


if __name__ == '__main__':
    main()