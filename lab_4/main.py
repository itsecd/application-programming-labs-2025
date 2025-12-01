import argparse
import sys
import matplotlib.pyplot as plt
from brightness_processing import (
    load_image_paths, 
    process_brightness, 
    sort_by_brightness, 
    filter_by_brightness,
    create_brightness_ranges
)
from graphics import (
    create_graph,
    save_dataframe_to_csv, 
    save_plot_to_file
)


def parse_arguments() -> argparse.Namespace:
    """Парсинг аргументов командной строки."""
    parser = argparse.ArgumentParser(
        description='Анализ диапазона яркости изображений'
    )
    parser.add_argument(
        '--csv', 
        '-c', 
        type=str, 
        required=True, 
        help='Путь к CSV файлу с аннотациями'
    )
    parser.add_argument(
        '--ranges', 
        '-r', 
        type=str, 
        default="0-50,51-100,101-150,151-200,201-255",
        help='Диапазоны яркости в формате "мин-макс,мин-макс,..."'
    )
    return parser.parse_args()


def main() -> None:
    """Основная функция выполнения задания."""
    try:
        args = parse_arguments()
        print(f"CSV файл: {args.csv}")
        print(f"Диапазоны яркости: {args.ranges}")
        
        brightness_ranges = create_brightness_ranges(args.ranges)
        print(f"Создано {len(brightness_ranges)} диапазонов яркости:")
        
        for range_label, (min_val, max_val) in brightness_ranges.items():
            print(f"  {range_label}: от {min_val} до {max_val}")
        
        image_paths = load_image_paths(args.csv)
        print(f"Загружено {len(image_paths)} путей к изображениям")
        
        if not image_paths:
            print("Нет изображений для обработки")
            sys.exit(1)
        
        df = process_brightness(image_paths, args.csv, brightness_ranges)
        
        if df.empty:
            print("Нет данных для анализа")
            sys.exit(1)
        
        print(f"\nСтатистика обработки:")
        print(f"Успешно обработано: {len(df)}/{len(image_paths)} изображений")
        
        sorted_df = sort_by_brightness(df)
        print(f"\nДанные отсортированы по диапазону яркости")
        
        filtered_df = filter_by_brightness(df, min_range=100)
        print(
            f"После фильтрации (min_range=100): {len(filtered_df)} изображений"
        )
        
        print(f"\nРаспределение по диапазонам яркости:")
        range_stats = df['Brightness_range_label'].value_counts().sort_index()
        
        for range_label, count in range_stats.items():
            percentage = (count / len(df)) * 100
            print(f"  {range_label}: {count} изображений ({percentage:.1f}%)")
        
        print("\nСоздание графика...")
        fig = create_graph(df)
        
        print("\nСохранение результатов...")
        save_dataframe_to_csv(df, 'brightness_analysis.csv')
        save_plot_to_file(fig, 'brightness_histogram.png')
        
        print(f"\nСтруктура DataFrame:")
        print(f"Колонки: {list(df.columns)}")
        print(f"Размер: {df.shape[0]} строк, {df.shape[1]} колонок")
        print(f"\nПервые 5 строк:")
        print(df.head())
        
        if fig is not None:
            print("\nОтображение графика...")
            plt.show()
        else:
            print("\nНе удалось создать график")
        
    except Exception as e:
        print(f"Ошибка: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()