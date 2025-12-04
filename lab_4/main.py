import argparse

from amp_functions import (
    dataframe_read,
    create_max_amp,
    sort_by_amp_range,
    filter_by_amp_range,
    save_df,
    create_chart,
)


def parse_args():
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
        "-r",
        "--range",
        type=str,
        help="Фильтр по диапазону амплитуды, например '0.1-0.2'",
    )
    return parser.parse_args()


def main():
    try:
        args = parse_args()

        df = dataframe_read(args.input)
        df = create_max_amp(df)
        df = sort_by_amp_range(df)

        if args.range:
            df = filter_by_amp_range(df, args.range)

        save_df(df, args.output)
        create_chart(df, args.output)
    except Exception as e:
        print(f"Произошла ошибка: {e}")


if __name__ == "__main__":
    main()
