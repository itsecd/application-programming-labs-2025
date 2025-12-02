import os
import argparse
from typing import List
from data_processor import DataFrameProcessor
from visualizer import HistogramPlotter


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Анализ яркости изображений.")
    parser.add_argument(
        "--bins",
        type=str,
        default="50,100,150,200",
        help="Границы диапазонов через запятую (напр. 80,160,240)"
    )
    return parser.parse_args()


def parse_bins_string(bins_str: str) -> List[int]:
    """Преобразует строку bins в список."""
    try:
        bins = sorted(list(set(int(x.strip()) for x in bins_str.split(',') if x.strip().isdigit())))

        valid_bins = [b for b in bins if 0 <= b < 255]

        if not valid_bins:
            print("Предупреждение: введены некорректные диапазоны. Используются стандартные.")
            return [50, 100, 150, 200]

        return valid_bins
    except Exception:
        print("Ошибка парсинга диапазонов. Используются стандартные.")
        return [50, 100, 150, 200]


def find_annotation_file(start_path: str) -> str:
    filename = "annotation.csv"
    if os.path.exists(os.path.join(start_path, filename)):
        return os.path.join(start_path, filename)
    parent = os.path.dirname(start_path)
    if os.path.exists(os.path.join(parent, "lab2", filename)):
        return os.path.join(parent, "lab2", filename)
    return ""


def main() -> None:
    args = parse_arguments()
    user_bins = parse_bins_string(args.bins)

    current_dir = os.path.dirname(os.path.abspath(__file__))
    input_csv = find_annotation_file(current_dir)
    output_plot = os.path.join(current_dir, "brightness_histogram.png")
    output_csv = os.path.join(current_dir, "analyzed_data.csv")

    if not input_csv:
        print("Ошибка: annotation.csv не найден.")
        return

    try:
        processor = DataFrameProcessor(input_csv)
        processor.rename_columns()

        print(f"Используемые границы диапазонов: {user_bins}")
        processor.add_brightness_ranges(user_bins)

        sorted_df = processor.sort_by_column('r_range')

        bin_order = processor.get_bin_order()

        plotter = HistogramPlotter(processor.df, bin_order)
        plotter.plot_rgb_histograms(output_plot, sorted_df)

        processor.save_csv(output_csv)
        print("Готово.")

    except Exception as e:
        print(f"Ошибка: {e}")


if __name__ == "__main__":
    main()