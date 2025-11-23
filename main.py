import argparse
from typing import Tuple

from image_processor import ImageProcessor
from visualization import ImageVisualizer


def main() -> None:
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
    parser.add_argument(
        '--channels', type=str, default='2,0,1',
        help='Новый порядок каналов (например: 2,0,1 для R->G, G->B, B->R)'
    )
    
    args = parser.parse_args()

    print("=== Обработка изображения ===")
    print(f"Входной файл: {args.input}")
    print(f"Выходной файл: {args.output}")
    print(f"Порядок каналов: {args.channels}")

    try:
        # Парсинг порядка каналов
        channel_order = tuple(int(x.strip()) for x in args.channels.split(','))
        
        # Проверка валидности порядка каналов
        if len(channel_order) != 3:
            raise ValueError("Должно быть указано ровно 3 канала")
        if not all(0 <= x <= 2 for x in channel_order):
            raise ValueError("Каналы должны быть в диапазоне 0-2")
        if len(set(channel_order)) != 3:
            raise ValueError("Все каналы должны быть уникальными")

        processor = ImageProcessor()
        original_image, processed_image = processor.swap_channels(
            args.input, channel_order
        )

        print(f"Размер изображения: {original_image.shape}")

        visualizer = ImageVisualizer()
        visualizer.show_comparison(
            original_image, processed_image, args.input, channel_order
        )

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