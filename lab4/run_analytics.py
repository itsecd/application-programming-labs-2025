import os
import sys
from data_processor import DataFrameProcessor
from visualizer import HistogramPlotter


def find_annotation_file(start_path: str, filename: str = "annotation.csv") -> str:
    """
    Автоматически ищет файл аннотации в текущей папке или в папке lab2.
    """
    current_path = os.path.join(start_path, filename)
    if os.path.exists(current_path):
        return current_path

    parent = os.path.dirname(start_path)
    candidate_lab2 = os.path.join(parent, "lab2", filename)
    if os.path.exists(candidate_lab2):
        return candidate_lab2

    return None


def main() -> None:
    """
    Основная точка входа в программу.
    """
    # Пути
    current_dir = os.path.dirname(os.path.abspath(__file__))
    input_csv_path = find_annotation_file(current_dir)

    output_csv = os.path.join(current_dir, "analyzed_data.csv")
    output_plot = os.path.join(current_dir, "brightness_histogram.png")

    if not input_csv_path:
        print("ОШИБКА: Файл annotation.csv не найден.")
        return

    try:
        processor = DataFrameProcessor(input_csv_path)
        print(f"Загружено записей: {len(processor.df)}")

        processor.rename_columns()

        processor.add_brightness_ranges()

        sorted_df = processor.sort_by_column(column='r_range', ascending=True)
        print("Данные отсортированы по колонке 'r_range'.")

        plotter = HistogramPlotter(processor.df)
        plotter.plot_rgb_histograms(output_plot, sorted_df)

        sorted_df.to_csv(output_csv, index=False)
        print(f"Итоговая таблица сохранена в {output_csv}")

    except KeyError as ke:
        print(f"ОШИБКА: Отсутствует необходимая колонка: {ke}")
    except FileNotFoundError as fnf:
        print(f"ОШИБКА: Файл не найден: {fnf}")
    except Exception as e:
        print(f"Непредвиденная ошибка: {e}")


if __name__ == "__main__":
    main()