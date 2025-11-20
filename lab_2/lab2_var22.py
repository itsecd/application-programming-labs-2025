import argparse
import re
import requests
import csv
from pathlib import Path

from bs4 import BeautifulSoup


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-c", "--csv", dest="csv_file", type=str, default="out.csv", help="название для CSV"
    )
    parser.add_argument(
        "-d", "--dir", dest="directory", type=str, default="downloaded_mp3", help="директория с файлами mp3"
    )

    return parser.parse_args()


def parse_html() -> BeautifulSoup | None:
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/58.0.3029.110 Safari/537.36"
        )
    }
    response = requests.get("https://mixkit.co/free-stock-music/pop/", headers=headers)
    if response.ok:
        return BeautifulSoup(response.text, "html.parser")
    return None


def csv_writer(file_paths: list[Path], filename: Path, out: Path) -> None:
    """
    Запись пути в csv файл
    """

    with filename.open(mode="w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["filename", "relative_path", "absolute_path"])
        for file_path in file_paths:
            absolute = file_path.resolve()
            relative = absolute.relative_to(Path.cwd())
            writer.writerow([file_path.name, str(relative), str(absolute)])


def extract_mp3(soup: BeautifulSoup) -> list[Path]:
    """
    Скачивает mp3 жанра pop
    """

    mp3_urls = []

    for script in soup.find_all("script", type="application/ld+json"):
        mp3_links = re.findall(r'"url"\s*:\s*"([^"]+\.mp3)"', script.string)
        for link in mp3_links:
            mp3_urls.append(link)

    return mp3_urls


class IteratorFile:
    """
    Итерируемый класс
    """

    def __init__(self, src: Path) -> None:
        self.src = src
        self.file_paths: list[str] = []
        self.index = 0

        if self.src.is_dir():
            self.file_paths = sorted([f for f in self.src.glob("*.mp3") if f.is_file()])
        elif self.src.suffix == ".csv":
            self.load_from_csv(src)

    def __iter__(self) -> "IteratorFile":
        self.index = 0
        return self

    def __next__(self) -> Path:
        if self.index >= len(self.file_paths):
            raise StopIteration
        current = self.file_paths[self.index]
        self.index += 1
        return current

    def load_from_csv(self, filename: Path) -> None:
        with filename.open("r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                absolute = row.get('absolute_path')
                if absolute:
                    self.file_paths.append(absolute)



def mp3_downloader() -> list[Path]:
    """
    Скачиваем mp3 и делаем список
    """

    files = []
    soup = parse_html()
    extracted = extract_mp3(soup)
    mkdir_path = Path("downloaded_mp3")
    mkdir_path.mkdir(exist_ok=True)
    for link in extracted:
        filename = Path(link).name
        mp3_file = mkdir_path / filename
        responce = requests.get(link)
        with mp3_file.open("wb") as file:
            file.write(responce.content)
        files.append(mp3_file)
    return files


def main():
    try:
        args = parse_arguments()

        csv_file = args.csv_file
        iter = IteratorFile(Path(csv_file))
        for i in iter:
            print(i)


    except Exception as ex:
        print("Ошибка: ", ex)


if __name__ == "__main__":
    main()
