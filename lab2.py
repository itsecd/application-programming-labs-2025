import argparse
import csv
from pathlib import Path
import requests
from bs4 import BeautifulSoup


class SimpleIterator:
    """
    итератор по путям к файлам
    """
    def __init__(self, source: Path):
        self.source = source
        self.file_paths: list[Path] = []
        self.counter = 0


        if self.source.is_dir():
            self.download_from_dir()
        
        elif self.source.is_file():
            self.download_from_csv()


    def download_from_dir(self) -> None:
        """
        ищет mp3 файлы в директории и сохраняет их в список
        """
        for file_path in self.source.rglob("*.mp3"):
            if file_path.is_file():
                self.file_paths.append(file_path)


    def download_from_csv(self) -> None:
        """
        читает пути к файлам из csv и сохраняет их в список
        """
        keys = ['absolute_path', 'relative_path', 'filename']

        with self.source.open(mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                for key in keys:
                    if key in row:
                        self.file_paths.append(Path(row[key]))
                        break        


    def __iter__(self) -> "SimpleIterator":
        return self


    def __next__(self) -> Path:
        if self.counter < len(self.file_paths):
            res = self.file_paths[self.counter]
            self.counter += 1
            return res
        else:
            raise StopIteration


def download_mp3(url: str, attribute_name: str, out_dir: Path) -> list[Path]:
    """
    Cкачивает mp3 и возвращает список файлов.
    """
    soup = extract_html(url)
    urls = extract_audio_urls(soup, attribute_name)
    if not urls:
        raise RuntimeError("mp3 не найдено")

    out_dir.mkdir()
    files = []
    for audio_url in urls:
        filename = Path(audio_url).name
        audio_file = out_dir / filename

        response = requests.get(audio_url)
        with audio_file.open(mode='wb') as file:
            file.write(response.content)
        files.append(audio_file)
    return files


def extract_html(url: str) -> BeautifulSoup:
    """
    загружает страницу и возвращает beautifulsoup
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    response = requests.get(url, headers=headers)
    return BeautifulSoup(response.text, "lxml")


def extract_audio_urls(soup: BeautifulSoup, attribute_name: str) -> list[str]:
    """
    извлекает из html ссылки на mp3
    """
    urls = []

    all_divs = soup.find_all("div", attrs={attribute_name: True})
    for div_tag in all_divs:
        link_value = div_tag.get(attribute_name)
        if link_value is not None:
            urls.append(link_value)
    return urls


def write_annotation(files: list[Path], csv_path: Path, base_dir: Path) -> None:
    """
    создаёт csv аннотацию
    """
    with csv_path.open(mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["filename", "absolute_path", "relative_path"])
        for path in files:
            abs_path = path.resolve()
            rel_path = abs_path.relative_to(resolved_base_dir)
            writer.writerow([path.name, str(abs_path), str(rel_path)])


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("-o", "--out", type=str, default="nature sounds", help="path to the output folder")
    parser.add_argument("-c", "--csv", type=str, default="annotation.csv", help="name of file for csv annotation")
    args = parser.parse_args()
    
    nature_url = "https://mixkit.co/free-sound-effects/nature/"
    
    print(f"output folder: {args.out}")
    print(f"csv file: {args.csv}")
    
    out_dir = Path(args.out)
    csv_path = Path(args.csv)

    try:
        files = download_mp3(nature_url, "data-audio-player-preview-url-value", out_dir)
        iterator = SimpleIterator(out_dir)
        write_annotation(list(iterator), csv_path, out_dir)
    except Exception as error:
        print(f"Ошибка: {error}")

if __name__ == "__main__":
    main()