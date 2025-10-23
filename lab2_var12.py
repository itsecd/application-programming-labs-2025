import argparse
import os
import csv
from icrawler.builtin import BingImageCrawler


def argparse_keywords() -> argparse.Namespace:
    """ "
    функция для парсинга путей, количества изображений и ключевых слов
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("file_save", type=str, help="путь к файлу сохранения фото")
    parser.add_argument("annotation", type=str, help="путь к файлу аннотации")
    parser.add_argument("number", type=int, help="количество изображений(от 50 до 100)")
    parser.add_argument("keywords", nargs="*", help="ключевые слова")
    args = parser.parse_args()
    if not (50 <= args.number <= 1000):
        raise ValueError("Количество изображений должно быть от 50 до 1000")
    return args


def add_img(keywords: list[str], file_save: str, number: int) -> list[dict[str, str]]:
    """
    функция для скачивания изображений
    """
    data = []
    for keyword in keywords:
        folder = os.path.join(file_save, keyword)
        crawler = BingImageCrawler(storage={"root_dir": folder})
        crawler.crawl(keyword=keyword, max_num=number)
        for root, _, files in os.walk(folder):
            for file_1 in files:
                if file_1.lower().endswith((".jpg", ".jpeg", ".png", ".gif")):
                    abs_path = os.path.abspath(os.path.join(root, file_1))
                    rel_path = os.path.relpath(abs_path, file_save)
                    data.append(
                        {
                            "absolute_path": abs_path,
                            "relative_path": rel_path,
                            "keyword": keyword,
                        }
                    )
    return data


class Iterator_csv:
    def __init__(self, annotation):
        self.annotation = annotation
        self.data = []
        self.index = 0
        with open(annotation, mode="r", encoding="utf-8", newline="") as f:
            read = csv.DictReader(f)
            self.data = list(read)

    def __iter__(self):
        return self

    def __next__(self):
        if self.index >= len(self.data):
            raise StopIteration
        value = self.data[self.index]
        self.index += 1
        return value


def append_annotation_file(annotation: str, data: list[dict]) -> None:
    """
    функция для добавления в файл анотации
    """
    fieldnames = ["absolute_path", "relative_path", "keyword"]
    with open(annotation, mode="w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames)
        writer.writeheader()
        writer.writerows(data)


def main() -> None:
    args = argparse_keywords()
    data = add_img(args.keywords, args.file_save, args.number)
    append_annotation_file(args.annotation, data)
    test = Iterator_csv(args.annotation)
    try:
        for val in test:
            print(val)
            print()
    except Exception as ex:
        print(f"Произошла ошибка: {ex}")


if __name__ == "__main__":
    main()
