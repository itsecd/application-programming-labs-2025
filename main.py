import argparse
from pathlib import Path

from core import download_images, create_annotation_csv
from paths_iterator import ImageList


def main():
    """Основная функция CLI интерфейса."""
    parser = argparse.ArgumentParser(description="Загрузка изображений")
    parser.add_argument("--keyword", type=str, default="cat")
    parser.add_argument("--num_images", type=int, default=50)
    parser.add_argument("--min_size", type=int, nargs=2, default=[200, 200])
    parser.add_argument("--max_size", type=int, nargs=2, default=[5000, 5000])
    parser.add_argument("--save_dir", type=str, default="./images")
    parser.add_argument("--csv_path", type=str, default="./annotation.csv")

    a = parser.parse_args()

    if not (50 <= a.num_images <= 1000):
        print("Количество изображений должно быть от 50 до 1000.")
        return

    download_images(
        a.keyword,
        a.num_images,
        tuple(a.min_size),
        tuple(a.max_size),
        a.save_dir
    )

    count = create_annotation_csv("try_image", a.csv_path)
    print(f"CSV создан: {a.csv_path}, файлов: {count}")

    print("\nПримеры файлов:")
    iterator = ImageList("try_image")
    for i, p in enumerate(iterator):
        if i >= 5:
            break
        print(f"{i+1}. {Path(p).name}")

    print("\nГотово.")


if __name__ == "__main__":
    main()