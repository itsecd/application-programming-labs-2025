import requests
from func import (get_args, run_downloads, print_summary)


def main(out_dir: str, csv_out: str) -> None:
    """Основная функция."""
    genres = ["country", "funk", "classical"]
    stats = run_downloads(out_dir, csv_out, genres)
    print_summary(csv_out, stats)


if __name__ == "__main__":
    args = get_args()
    try:
        main(args.output, args.csv)
    except FileNotFoundError as err:
        print(f'Файл не найден: "{err.filename}"')
    except requests.RequestException as err:
        print(f"Ошибка сети: {err}")
    except Exception as err:
        print(f"Непредвиденная ошибка: {err}")
