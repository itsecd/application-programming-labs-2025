import argparse

import data_processing
import dataframe_utility
import visualization


def parse_arguments() -> argparse.Namespace:
    """
    Adds and parses command-line arguments.
    """
    parser = argparse.ArgumentParser(description="Tool to analyze data from CSV annotation.")
    parser.add_argument(
        '--annotation_path',
        '-a',
        required=True,
        help='Filepath to the original CSV annotation.'
    )
    parser.add_argument(
        '--output_csv_path',
        '-oc',
        default='analysis_results.csv',
        help='Filepath to save the DataFrame in CSV.'
    )
    parser.add_argument(
        '--output_plot_path',
        '-op',
        default='brightness_histogram.png',
        help='Filepath to save the histogram.'
    )
    parser.add_argument(
        '--brightness_range',
        '-br',
        default=[0, 127, 256],
        nargs='+',
        type=int,
        help='Brightness ranges to filter by (e.g.: 0 67 140 256)'
    )
    parser.add_argument(
        '--filter_range',
        '-f',
        default="0-126",
        help='Brightness range to filter by (e.g.: 0-66)'
    )
    return parser.parse_args()


def main() -> None:
    """
    Main function.
    """
    args = parse_arguments()

    print("Args for script:")
    print(f"    Filepath to the original CSV annotation: '{args.annotation_path}'")
    print(f"    Filepath to save the DataFrame in CSV: '{args.output_csv_path}'")
    print(f"    Filepath to save the histogram: '{args.output_plot_path}'")
    print(f"    Brightness ranges: '{args.brightness_range}'")
    print(f"    Brightness range to filter by: '{args.filter_range}'")

    try:
        original_dataframe = data_processing.load_data(args.annotation_path)
        enriched_dataframe = data_processing.enrich_data(original_dataframe)
        dataframe = data_processing.add_range(enriched_dataframe, args.brightness_range)

        df_sorted = dataframe_utility.sort_by_brightness(dataframe)
        df_filtered = dataframe_utility.filter_by_brightness_range(df_sorted, args.filter_range)

        print("\nOriginal DataFrame: ")
        print(dataframe.head())
        print("\nSorted DataFrame: ")
        print(df_sorted.head())
        print("\nFiltered DataFrame: ")
        print(df_filtered)

        data_processing.save_data(df_sorted, args.output_csv_path)

        visualization.plot_histogram(df_sorted, args.output_plot_path)

    except FileNotFoundError as e:
        print(f"File error: {e}")
    except KeyError as e:
        print(f"Data error. Required column is missing in DataFrame: {e}")
    except Exception as e:
        print(f"Error occurred: {e}")


if __name__ == "__main__":
    main()
