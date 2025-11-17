import argparse
from downloader import MusicDownloader
from iterator_module import FileIterator

def main() -> None:
    parser = argparse.ArgumentParser(description="Скачивание музыки с mixkit.co по длительности")
    parser.add_argument("--folder", type=str, default="./downloads", help="Папка для сохранения треков")
    parser.add_argument("--csv", type=str, default="./annotation.csv", help="CSV-аннотация")
    parser.add_argument("--count", type=int, default=50, help="Количество треков для скачивания")
    parser.add_argument("--min_duration", type=int, default=30, help="Минимальная длительность (сек)")
    parser.add_argument("--max_duration", type=int, default=180, help="Максимальная длительность (сек)")
    args = parser.parse_args()

    print(f"🎵 Начинаем скачивание до {args.count} треков длительностью от {args.min_duration} до {args.max_duration} сек...")

    downloader = MusicDownloader(args.folder)
    downloader.download_music(
        count=args.count,
        min_sec=args.min_duration,
        max_sec=args.max_duration,
        csv_path=args.csv
    )

    print(f"🔁 Проверка итератора:")
    for path in FileIterator(args.csv):
        print("  ", path)

if __name__ == "__main__":
    main()