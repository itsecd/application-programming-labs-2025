# main_lab.py
from dataframe import (create_dataframe_from_annotation,
                       name_columns,
                       add_brightness_columns,
                       save_dataframe)
import os
from parser import parse_args
from sort_and_filter import sort_dataframe_by_brightness, filter_dataframe_by_brightness
import sys
from visualization import plot_brightness_data


def main():

    try:
        args = parse_args()

        if not os.path.exists(args.input):
            raise FileNotFoundError(f"Ошибка: Файл не найден по пути: '{args.input}'")

        if not os.path.isfile(args.input):
            raise ValueError(f"Ошибка: Указанный путь '{args.input}'"
                             f" является директорией, а не файлом.")

        _, ext = os.path.splitext(args.input)

        if ext.lower() != '.csv':
            raise ValueError(f"Ошибка: Файл '{args.input}' имеет некорректное расширение"
                             f" '{args.input}'. Ожидается '.csv'.")

        df = create_dataframe_from_annotation(args.input)
        
        if df.empty:
            print("DataFrame пуст")
            sys.exit(1)

        df = name_columns(df, "absolute_path", "relative_path")

        df = add_brightness_columns(df, "absolute_path")

        df_sorted = sort_dataframe_by_brightness(df, "R")

        df_filtered = filter_dataframe_by_brightness(df_sorted,
                                                     min_val=50,
                                                     max_val=150,
                                                     column_name="R")

        plot_brightness_data(df_filtered, args.output)

        save_dataframe(df_filtered, output_file='final_processed_data.csv')

    except FileNotFoundError as e:
        print(e)
        sys.exit(1)
    except ValueError as e:
        print(e)
        sys.exit(1)
    except Exception as e:
        print(f"Произошла непредвиденная ошибка: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()