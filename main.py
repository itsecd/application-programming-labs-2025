import argparse

from core import download_images, create_annotation_csv
from paths_iterator import ImageList


def main():
    """Основная функция CLI интерфейса."""
    parser = argparse.ArgumentParser(description="Загрузка изображений")
    parser.add_argument("--keyword", type=str, default="cat")
    parser.add_argument("--num_images", type=int, default=50)

    args = parser.parse_args()

    if not (50 <= args.num_images <= 1000):
        print("Количество изображений должно быть от 50 до 1000.")
        return

    download_images(
        args.keyword,
        args.num_images,
        (200, 200),
        (5000, 5000),
        "./images"
    )

    print("Загрузка завершена.")


if __name__ == "__main__":
    main()