from __future__ import annotations
import argparse
import sys
from pathlib import Path
import pandas as pd

from analyzer import (
    create_dataframe_from_folder,
    create_dataframe_from_csv,
    sort_by_aspect_ratio,
    filter_by_aspect_ratio
)
from plotter import plot_aspect_ratios

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Анализ отношения сторон изображений в папке"
    )
    parser.add_argument("folder", nargs="?", type=str, help="Путь к папке с изображениями")
    parser.add_argument("--csv", type=str, help="Загрузить готовый анализ из CSV")
    parser.add_argument(
        "--sort", choices=['asc', 'desc'], default='desc',
        help="Сортировка по aspect_ratio: asc — по возрастанию, desc — по убыванию"
    )
    parser.add_argument("--min", type=float, help="Минимальное отношение сторон")
    parser.add_argument("--max", type=float, help="Максимальное отношение сторон")

    args = parser.parse_args()

    try:
        if args.csv:
            if not Path(args.csv).exists():
                raise FileNotFoundError(f"CSV-файл не найден: {args.csv}")
            df = create_dataframe_from_csv(args.csv)
            print(f"Загружено из CSV: {len(df)} записей")
        elif args.folder:
            df = create_dataframe_from_folder(args.folder)
        else:
            parser.error("Укажите либо папку с изображениями, либо --csv файл")

        if df.empty:
            print("Предупреждение: DataFrame пустой — изображения не найдены.")
            sys.exit(1)

        print(f"Всего найдено изображений: {len(df)}")
        print(df[['filename', 'width_px', 'height_px', 'aspect_ratio']].head(10))

        df_sorted = sort_by_aspect_ratio(df, ascending=(args.sort == 'asc'))
        df_final = filter_by_aspect_ratio(df_sorted, args.min, args.max)

        df_final.to_csv("images_analysis.csv", index=False, encoding='utf-8-sig')
        df_final.to_excel("images_analysis.xlsx", index=False)
        print(f"\nРезультаты сохранены ({len(df_final)} строк):")

        plot_aspect_ratios(df_sorted)

    except Exception as e:
        raise


if __name__ == "__main__":
    main()