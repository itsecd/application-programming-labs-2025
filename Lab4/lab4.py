import argparse


import data_frame_operations
import sort_and_filter
import make_graph


def parsing() -> tuple[str, str]:
        """парсер"""
        parser = argparse.ArgumentParser()
        parser.add_argument("file_path", type=str, help="Enter file path")
        args = parser.parse_args()
        return args.file_path


def main():
    try:
        file_path = parsing()
        data_frame = data_frame_operations.create_DataFrame(file_path)
        data_frame = data_frame_operations.area_distrib(data_frame)
        data_frame = sort_and_filter.filter_by_area(data_frame, 3500, 7766200)
        data_frame = sort_and_filter.df_sort(data_frame, "area")
        data_frame = make_graph.add_range_column(data_frame)
        make_graph.make_histogram(data_frame)
    except Exception as exp:
        print(exp)


if __name__ == "__main__":
    main()
