import os
import random
import argparse

from icrawler.builtin import BingImageCrawler


def download_colored_snakes(colors: list[str], total_count: int, output_dir: str) -> None:
    """
    Скачивание изображений змей разных цветов в одну папку
    """

    if not 50 <= total_count <= 1000:
        raise ValueError("Общее количество должно быть от 50 до 1000")
    
    os.makedirs(output_dir, exist_ok=True)
    print(f"Папка создана: {os.path.abspath(output_dir)}")

    counts = [1] * len(colors)
    for _ in range(total_count - len(colors)):
        counts[random.randint(0, len(colors) - 1)] += 1

    print(f"Общее количество: {total_count}")
    print("Распределение по цветам:")
    for color, count in zip(colors, counts):
        print(f"  {color}: {count}")
    

    for color, count in zip(colors, counts):
        print(f"Скачиваем {count} изображений цвета '{color}'...")
        
        crawler = BingImageCrawler(storage={'root_dir': output_dir})
        crawler.crawl(keyword=f"snake {color}", max_num=count)


def main() -> None:
    parser = argparse.ArgumentParser(description='Скачивание изображений змей по цветам')
    parser.add_argument('-c', '--colors', nargs='+', required=True,
                       help='Список цветов для поиска')
    parser.add_argument('-t', '--total_count', type=int, required=True,
                       help='Общее количество изображений (50-1000)')
    parser.add_argument('-o', '--output_dir', type=str, default='snake_images',
                       help='Папка для сохранения изображений')
    
    args = parser.parse_args()
    
    try:
        download_colored_snakes(args.colors, args.total_count, args.output_dir)
        print("Готово! Все изображения скачаны.")
    except Exception as e:
        print(f"Произошла ошибка: {e}")


if __name__ == "__main__":
    main()