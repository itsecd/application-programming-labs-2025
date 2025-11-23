import argparse
from typing import Iterator


class AnnotationIterator:


    def __init__(self, source: str):
        """
        задание источника 
        """
        self.source = source
        self.index = 0
        self.data = []

    def __iter__(self) -> Iterator[str]:
        """ 
        возврат итератора 
        """
        return self

    def __next__(self) -> str:
        """ 
        получение следующего элемента 
        """
        if self.index >= len(self.data):
            raise StopIteration

        value = self.data[self.index]
        self.index += 1
        return value


def download_images(ranges: list[str], directory: str) -> None:
    """ 
    установка изображений 
    """
    pass


def make_grayscale(directory: str) -> None:
    """ 
    перевод в полутон 
    """
    pass


def write_csv(annotation: str, directory: str) -> None:
    """ 
    создание аннотации 
    """
    pass


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("keyword", type=str)
    parser.add_argument("annotation", type=str)
    parser.add_argument("ranges", nargs="+")
    return parser.parse_args()


def main():
    args = parse_args()

    print("Аргументы получены:")
    print(args)


if __name__ == "__main__":
    main()
