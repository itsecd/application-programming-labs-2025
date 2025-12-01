import argparse

from utils import (
    load_annotation_data,
    add_brightness_column,
    add_brightness_range_column,
    sort_by_brightness,
    filter_by_brightness_range,
    create_histogram,
    save_dataframe
)


def parse_arguments():
    """
    Парсинг аргументов командной строки.
    """

    parser = argparse.ArgumentParser(description="Анализ яркости изображений")
    
    parser.add_argument('--annotation', '-a', required=True,
                       help='Путь к файлу аннотации CSV')
    
    parser.add_argument('--output_csv', '-oc', default='analysis_results.csv',
                       help='Путь для сохранения результатов в CSV')
    
    parser.add_argument('--output_plot', '-op', default='brightness_histogram.png',
                       help='Путь для сохранения гистограммы')
    
    parser.add_argument('--bins', '-b', nargs='+', type=int, default=[0, 51, 102, 153, 204, 256],
                       help='Границы диапазонов яркости')
    
    parser.add_argument('--filter_range', '-f',
                       help='Диапазон для фильтрации')
    
    parser.add_argument('--show', action='store_true',
                       help='Показать график')

    return parser.parse_args()


def main() -> None:
    """
    Основная функция программы.
    """

    args = parse_arguments()

    try:
        df = load_annotation_data(args.annotation)
        print(f"Загружено изображений: {len(df)}")
        
        df = add_brightness_column(df)
        print(f"Успешно обработано изображений: {len(df)}")
        
        df, brightness_labels = add_brightness_range_column(df, args.bins)
        print(f"Диапазоны яркости: {', '.join(brightness_labels)}")

        df_sorted = sort_by_brightness(df)
        
        if args.filter_range:
            if args.filter_range in brightness_labels:
                df_filtered = filter_by_brightness_range(df_sorted, args.filter_range)
                print(f"\nРезультат фильтрации по диапазону '{args.filter_range}':")
                print(f"Найдено изображений: {len(df_filtered)}")
                if len(df_filtered) > 0:
                    print(df_filtered[['relative_path', 'brightness', 'brightness_range']].head())
            else:
                print(f"\nДиапазон '{args.filter_range}' не найден")
                print(f"Доступные диапазоны: {', '.join(brightness_labels)}")

        create_histogram(df_sorted, args.output_plot, args.show)
        print(f"Гистограмма: {args.output_plot}")
        
        save_dataframe(df_sorted, args.output_csv)
        print(f"Данные: {args.output_csv}")

    except FileNotFoundError as e:
        print(f"Ошибка: {e}")
    except Exception as e:
        print(f"Произошла ошибка: {e}")


if __name__ == "__main__":
    main()