import argparse

import make_graph
import sort_and_filter
import make_data_and_add


def parsing() -> tuple[str, str]:
    """
    передача аргументов через командную строку
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("filename_data", type=str)
    args = parser.parse_args()
    return args.filename_data


def main() -> None:
    try:
        data_file_name = parsing()
        df = make_data_and_add.create_DataFrame(data_file_name)
        make_data_and_add.distribution_brightness_columns(df)
        filters = {"red_min": 123}
        sort_and_filter.filter(filters, df)
        make_graph.sorted_graph(df)
        make_graph.make_histogram(df)
        df.to_csv("dataframe.csv")
    except Exception as exp:
        print(exp)


if __name__ == "__main__":
    main()

