import argparse
from functions import read_annotation_file, calculate_aspect_ratios, add_range_column, sort_by_aspect_ratio, filter_by_range, create_histogram

def main():
    
    try:
        # Парсинг аргументов командной строки
        parser = argparse.ArgumentParser(description='Анализ соотношений сторон изображений')
        parser.add_argument('--bins', nargs='+', type=float, required=True,
                          help='Границы диапазонов через пробел (например: 0.5 1.0 1.5 2.0 2.5)')
        parser.add_argument('--filter_range', type=str, required=False,
                          help='Диапазон для фильтрации (например: 1.0-1.5)')
        args = parser.parse_args()
        
        bins = args.bins
        range_filter = args.filter_range

        # Чтение данных из файла аннотации
        df = read_annotation_file('annotation.csv')
        print("Исходные данные:")
        print(df)

        # Добавление соотношения сторон
        df = calculate_aspect_ratios(df)

        # Добавление столбца с диапазонами
        df = add_range_column(df, bins)

        print("\nDataFrame с соотношениями сторон:")
        print(df)

        # Сортировка данных
        df_sorted = sort_by_aspect_ratio(df)
        print("\nОтсортированный DataFrame:")
        print(df_sorted)

        # Фильтрация данных (если указан диапазон)
        if range_filter:
            df_filtered = filter_by_range(df, range_filter)
            print(f"\nФильтрованный DataFrame ({range_filter}):")
            print(df_filtered)
        else:
            print("\nДиапазон для фильтрации не указан, пропускаем фильтрацию")

        # Построение гистограммы
        create_histogram(df)

        # Сохранение DataFrame
        df.to_csv('data.csv', index=False)

        print("\nДанные сохранены в 'data.csv'")
        print("График сохранен в 'histogram.png'")

    except Exception as e:
        print(f"Ошибка: {e}")

if __name__ == "__main__":
    main()
