import pandas as pd
import matplotlib.pyplot as plt
from functions import read_annotation_file, calculate_aspect_ratios, add_range_column, sort_by_aspect_ratio, filter_by_range

def main():
    
    try:
        # Чтение данных из файла аннотации
        df = read_annotation_file('annotation.csv')
        print("Исходные данные:")
        print(df)

        # Добавление соотношения сторон
        df = calculate_aspect_ratios(df)

        # Пользователь вводит диапазоны
        print("\nВведите границы диапазонов через пробел (например: 0.5 1.0 1.5 2.0 2.5):")
        user_input = input().split()
        bins = [float(x) for x in user_input]

        # Добавление столбца с диапазонами
        df = add_range_column(df, bins)

        print("\nDataFrame с соотношениями сторон:")
        print(df)

        # Сортировка данных
        df_sorted = sort_by_aspect_ratio(df)
        print("\nОтсортированный DataFrame:")
        print(df_sorted)

        # Фильтрация данных
        print("\nВведите диапазон для фильтрации (например: 1.0-1.5):")
        range_filter = input()
        df_filtered = filter_by_range(df, range_filter)
        print(f"\nФильтрованный DataFrame ({range_filter}):")
        print(df_filtered)

        # Построение гистограммы
        plt.figure(figsize=(8, 5))
        df['range'].value_counts().sort_index().plot(kind='bar')
        plt.title('Распределение по соотношению сторон')
        plt.xlabel('Диапазон соотношения')
        plt.ylabel('Количество изображений')

        # Сохранение и отображение графика
        plt.savefig('гистограмма.png')
        plt.show()

        # Сохранение DataFrame
        df.to_csv('данные.csv', index=False)

        print("\nДанные сохранены в 'данные.csv'")
        print("График сохранен в 'гистограмма.png'")

    except Exception as e:
        print(f"Ошибка: {e}")

if __name__ == "__main__":
    main()