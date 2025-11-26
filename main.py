import argparse
from calculations import (
    dataframe_read,
    create_min_amp,
    filtration_df,
    save_df,
    create_chart,
)


def parse_args() -> argparse.ArgumentParser:
    """
    Парсим аргументы для выполнения задания
    """
    parser = argparse.ArgumentParser()

    parser.add_argument("-i", "--input", type=str, help="Путь к файлу csv")

    parser.add_argument(
        "-o",
        "--output",
        type=str,
        default="output",
        help="Название файла для датафрейма",
    )

    parser.add_argument(
        "-f", "--filter", type=float, help="Фильтрация по минимальной амплитуде"
    )

    return parser.parse_args()


def main():
    try:
        args = parse_args()

        df = dataframe_read(args.input)
        df = create_min_amp(df)
        filtered = filtration_df(df, args.filter)
        save_df(filtered, args.output)
        create_chart(df, args.output)
    except Exception as e:
        print(f"Произошла ошибка: {e}")


if __name__ == "__main__":
    main()
