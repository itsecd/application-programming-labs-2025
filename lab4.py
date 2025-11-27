import argparse
from typing import Optional
from dataframe_utils import (
    create_dataframe_from_annotation,
    create_dataframe_from_folder,
    add_aspect_ratio_column,
    add_aspect_ratio_bins_column,
    sort_by_aspect_ratio,
    filter_by_aspect_ratio,
    plot_aspect_ratio_histogram,
    plot_aspect_ratio_sorted,
)


def parse_arguments() -> argparse.Namespace:
    """
    Парсит аргументы командной строки для анализа отношений сторон изображений

    Returns:
        argparse.Namespace: Объект с распарсенными аргументами
    """
    parser = argparse.ArgumentParser(description="Анализ отношений сторон изображений")
    parser.add_argument("--annotation", type=str, help="Путь к файлу аннотации CSV")
    parser.add_argument("--folder", type=str, help="Путь к папке с изображениями")
    parser.add_argument(
        "--output_df",
        type=str,
        default="image_analysis.csv",
        help="Путь для сохранения DataFrame (по умолчанию: image_analysis.csv)",
    )
    parser.add_argument(
        "--output_plot",
        type=str,
        default="aspect_ratio_plot.png",
        help="Путь для сохранения графика (по умолчанию: aspect_ratio_plot.png)",
    )
    parser.add_argument(
        "--min_ratio", type=float, help="Минимальное отношение сторон для фильтрации"
    )
    parser.add_argument(
        "--max_ratio", type=float, help="Максимальное отношение сторон для фильтрации"
    )

    return parser.parse_args()


def main() -> None:
    """Основная функция"""
    args: argparse.Namespace = parse_arguments()

    # Создаем DataFrame
    if args.annotation:
        df = create_dataframe_from_annotation(args.annotation)
    elif args.folder:
        df = create_dataframe_from_folder(args.folder)
    else:
        print("Ошибка: необходимо указать --annotation или --folder")
        return

    if df is None or df.empty:
        print("Не удалось создать DataFrame")
        return

    print(f"Создан DataFrame с {len(df)} изображениями")

    # Добавляем колонку с отношениями сторон
    df = add_aspect_ratio_column(df)
    print("Добавлена колонка aspect_ratio")

    # Добавляем колонку с диапазонами для гистограммы
    df = add_aspect_ratio_bins_column(df, bins=5)
    print("Добавлена колонка aspect_ratio_range")

    # Применяем фильтрацию если указаны параметры
    if args.min_ratio is not None or args.max_ratio is not None:
        df_filtered = filter_by_aspect_ratio(df, args.min_ratio, args.max_ratio)
        print(f"После фильтрации: {len(df_filtered)} изображений")
    else:
        df_filtered = df

    # Сортируем данные
    df_sorted = sort_by_aspect_ratio(df_filtered)
    print("Данные отсортированы по отношению сторон")

    # Сохраняем DataFrame
    df_sorted.to_csv(args.output_df, index=False, encoding="utf-8")
    print(f"DataFrame сохранен: {args.output_df}")

    # Строим и сохраняем график
    plot_aspect_ratio_histogram(df_sorted, args.output_plot)

    # Дополнительный график с отсортированными данными
    plot_output_sorted: str = args.output_plot.replace(".png", "_sorted.png")
    plot_aspect_ratio_sorted(df_sorted, plot_output_sorted)

    # Выводим статистику
    print("\nСТАТИСТИКА:")
    print(f"Всего изображений: {len(df)}")
    print(f"После фильтрации: {len(df_filtered)}")
    print(f"Минимальное отношение сторон: {df['aspect_ratio'].min():.2f}")
    print(f"Максимальное отношение сторон: {df['aspect_ratio'].max():.2f}")
    print(f"Среднее отношение сторон: {df['aspect_ratio'].mean():.2f}")

    print("\nРаспределение по диапазонам:")
    print(df["aspect_ratio_range"].value_counts())


if __name__ == "__main__":
    main()
