import os
import pandas as pd

from analysis import (
    get_args,
    build_dataframe,
    sort_dataframe,
    filter_dataframe,
    save_dataframe,
    plot_histogram,
)


def main(annotation_csv: str, dataframe_dir: str, graphics_dir: str) -> None:
    """Основная функция."""
    os.makedirs(dataframe_dir, exist_ok=True)
    os.makedirs(graphics_dir, exist_ok=True)

    df = build_dataframe(annotation_csv)
    df_path = save_dataframe(df, dataframe_dir, "analysis_dataframe.csv")
    print(f"Сохранён датафрейм: {df_path}")

    sorted_df = sort_dataframe(df, "Средняя амплитуда")
    sorted_path = save_dataframe(sorted_df, dataframe_dir, "sorted_dataframe.csv")
    print(f"Сохранён отсортированный датафрейм: {sorted_path}")

    first_range = sorted_df["Диапазон амплитуды"].iloc[0]
    filtered_df = filter_dataframe(sorted_df, "Диапазон амплитуды", first_range)
    filtered_path = save_dataframe(filtered_df, dataframe_dir, "filtered_dataframe.csv")
    print(f"Сохранён отфильтрованный датафрейм: {filtered_path}")

    plot_path = os.path.join(graphics_dir, "amplitude_histogram.png")
    plot_histogram(sorted_df, "Диапазон амплитуды", plot_path)
    print(f"Сохранён график: {plot_path}")


if __name__ == "__main__":
    args = get_args()

    try:
        main(
        annotation_csv=args.annotation_csv,
        dataframe_dir=args.dataframe_dir,
        graphics_dir=args.graphics_dir
        )
    except FileNotFoundError as err:
        print(f'Файл не найден: "{err.filename}"')
    except Exception as err:
        print(f"Непредвиденная ошибка: {err}")
