import argparse


from save_dataframe import save_dataframe
from creating_new_columns import creating_range_columns
from filter_sort import filtering_values, sort_range
from creating_graph_and_save import creating_graph_and_save
from creating_dataframe_and_columns import creating_dataframe_and_columns


def parse_argument() -> argparse.Namespace:
    """
    функция для парсинга
    """
    parse = argparse.ArgumentParser()
    parse.add_argument("fail", type=str, help="путь к файлу анотации")
    parse.add_argument(
        "fail_save_data", type=str, help="путь к файлу сохранения датафрейма"
    )
    parse.add_argument(
        "fail_save_chart", type=str, help="путь к файлу сохранения графика"
    )
    args = parse.parse_args()
    return args


def main() -> None:
    args = parse_argument()

    df = creating_dataframe_and_columns(args.fail)

    df = creating_range_columns(df)

    df_filtered = filtering_values(df, "range_b", min_values=100, max_values=255)

    df_sorted = sort_range(df_filtered, "range_r")

    save_dataframe(df_sorted, args.fail_save_data)
    print(df_sorted.index.tolist())
    creating_graph_and_save(df_sorted, args.fail_save_chart)


if __name__ == "__main__":
    main()
