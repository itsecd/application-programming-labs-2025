import argparse
import csv
import time
from pathlib import Path
from typing import List, Optional
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup

DEFAULT_CATEGORY_TEMPLATE = "https://mixkit.co/free-sound-effects/{category}/"
DEFAULT_CATEGORY = "animals"
DEFAULT_LIMIT = 50
DEFAULT_DELAY = 0.4


def get_soup(url: str, session: requests.Session) -> BeautifulSoup:
    """Получить BeautifulSoup объект страницы."""
    r = session.get(
        url,
        headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"},
        timeout=25,
    )
    r.raise_for_status()
    return BeautifulSoup(r.text, "html.parser")


def extract_download_targets(soup: BeautifulSoup, base_url: str) -> List[str]:
    """Извлечь цели для скачивания со страницы."""
    targets = []
    for btn in soup.select('button.download-button--icon'):
        rel = btn.get("data-download--button-modal-url-value")
        if rel:
            targets.append(urljoin(base_url, rel))
    return list(dict.fromkeys(targets))


def extract_audio_url(download_page_url: str, session: requests.Session) -> Optional[str]:
    """Извлечь URL аудиофайла со страницы загрузки."""
    soup = get_soup(download_page_url, session)

    for tag in soup.select('div.download-modal__wrapper'):
        val = tag.get("data-download--modal-url-value")
        if val:
            return urljoin(download_page_url, val)

    return None


def find_next_page(soup: BeautifulSoup, base_url: str) -> Optional[str]:
    """Найти следующую страницу."""
    a = soup.select_one('a[rel="next"]')
    if a and a.get("href"):
        return urljoin(base_url, a["href"])
    return None


def download_file(url: str, save_dir: Path, session: requests.Session) -> Optional[Path]:
    """Скачать файл."""
    save_dir.mkdir(parents=True, exist_ok=True)

    try:
        with session.get(
            url,
            stream=True,
            timeout=40,
            allow_redirects=True,
            headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
        ) as r:
            r.raise_for_status()

            name = Path(urlparse(url).path).name or "sound.mp3"
            if not any(name.lower().endswith(ext) for ext in (".mp3", ".wav")):
                name += ".mp3"

            out = save_dir / name
            with out.open("wb") as f:
                for chunk in r.iter_content(chunk_size=32768):
                    if chunk:
                        f.write(chunk)
            return out
    except Exception:
        return None


def crawl_category(save_dir: Path, category_url: str, limit: int, delay: float) -> List[Path]:
    """Скачать файлы из категории."""
    session = requests.Session()
    downloaded: List[Path] = []
    next_url: Optional[str] = category_url

    while next_url and len(downloaded) < limit:
        soup = get_soup(next_url, session)
        targets = extract_download_targets(soup, next_url)

        for target in targets:
            if len(downloaded) >= limit:
                break

            if target.lower().endswith(".wav"):
                file_path = download_file(target, save_dir, session)
            else:
                audio_url = extract_audio_url(target, session)
                file_path = download_file(audio_url, save_dir, session) if audio_url else None

            if file_path:
                downloaded.append(file_path)
                time.sleep(delay)

        next_url = find_next_page(soup, next_url)

    return downloaded


def write_annotation_csv(csv_path: Path, root_dir: Path, files: List[Path]) -> None:
    """Записать CSV файл с аннотациями скачанных файлов."""
    csv_path.parent.mkdir(parents=True, exist_ok=True)
    root_abs = root_dir.resolve()

    with csv_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["abs_path", "rel_path"])

        for file_path in files:
            abs_path = file_path.resolve()
            rel_path = abs_path.relative_to(root_abs)
            writer.writerow([str(abs_path), str(rel_path)])


class FilePathIterator:
    """
    Итератор по путям к файлам.
    - Если source указывает на CSV: читает колонку 'abs_path'
    - Если source указывает на папку: ищет *.mp3, *.wav (рекурсивно)
    """
    def __init__(self, source: Path):
        self._paths: List[Path] = []
        if source.is_file() and source.suffix.lower() == ".csv":
            with source.open("r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    p = row.get("abs_path")
                    if p:
                        self._paths.append(Path(p))
        elif source.is_dir():
            self._paths = sorted(
                list(source.rglob("*.mp3")) + list(source.rglob("*.wav"))
            )
        else:
            raise ValueError(f"Неподдерживаемый источник для итератора: {source}")
        self._i = 0

    def __iter__(self) -> "FilePathIterator":
        return self

    def __next__(self) -> Path:
        if self._i >= len(self._paths):
            raise StopIteration
        p = self._paths[self._i]
        self._i += 1
        return p


def main() -> None:
    """Основная функция."""
    parser = argparse.ArgumentParser(description="Скачать звуки с Mixkit")
    parser.add_argument("save_dir", help="Папка для сохранения")
    parser.add_argument("--limit", type=int, default=DEFAULT_LIMIT, help="Лимит файлов")
    parser.add_argument("--category", nargs="+", default=[DEFAULT_CATEGORY], help="Категории")
    parser.add_argument("--delay", type=float, default=DEFAULT_DELAY, help="Задержка")
    parser.add_argument("--csv", default="annotation.csv", help="Путь к CSV файлу для аннотаций")
    parser.add_argument(
        "--iterate",
        default=None,
        help="Источник для итератора: путь к CSV (abs_path, rel_path) или папке с файлами"
    )

    args = parser.parse_args()
    save_dir = Path(args.save_dir)

    all_downloaded_files: List[Path] = []

    for category in args.category:
        category_url = DEFAULT_CATEGORY_TEMPLATE.format(category=category)
        files = crawl_category(save_dir / category, category_url, args.limit, args.delay)
        all_downloaded_files.extend(files)
        print(f"[{category}]: {len(files)} файлов")

    print(f"Всего скачано: {len(all_downloaded_files)} файлов")

    csv_path = Path(args.csv)
    write_annotation_csv(csv_path, save_dir, all_downloaded_files)
    print(f"CSV файл с аннотациями создан: {csv_path}")

    if args.iterate:
        src = Path(args.iterate)
        print(f"[Iterator] Источник: {src}")
        try:
            it = FilePathIterator(src)
            for p in it:
                print(p)
        except Exception as e:
            print(f"[Iterator] Ошибка: {e}")


if __name__ == "__main__":
    main()
