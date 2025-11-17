# main.py
import pandas as pd
import os
import sys
from pandas import DataFrame
from image_processor import calculate_brightness_range
from dataframe_operations import sort_by_brightness_range, filter_by_brightness_range
from plot_generator import create_brightness_plot


def load_and_process_data(input_file: str) -> DataFrame | None:
    """Загружает и обрабатывает данные из CSV файла."""
    if not os.path.exists(input_file):
        return None
    
    df = pd.read_csv(input_file)
    return df


def add_brightness_range_column(df: DataFrame) -> DataFrame:
    """Добавляет колонку с диапазоном яркости и удаляет строки с ошибками."""
    df['brightness_range'] = df['absolute_path'].apply(calculate_brightness_range)
    
    initial_count = len(df)
    df = df.dropna(subset=['brightness_range'])
    final_count = len(df)
    
    if initial_count != final_count:
        print(f"Предупреждение: {initial_count - final_count} изображений не удалось обработать")
    
    return df


def print_dataframe_info(df: DataFrame, title: str) -> None:
    """Выводит информацию о DataFrame."""
    print("=" * 60)
    print(title)
    print("=" * 60)
    print("DataFrame:")
    print(df.head())
    print(f"\nРазмер DataFrame: {df.shape}")
    print(f"Колонки: {list(df.columns)}")


def main() -> None:
    if len(sys.argv) != 2:
        print("Использование: python main.py <input_csv_file>")
        print("Пример: python main.py annotation.csv")
        sys.exit(1)
    
    input_file = sys.argv[1]
    
    # 1. Загрузка данных и формирование DataFrame
    df = load_and_process_data(input_file)
    if df is None:
        print(f"Ошибка: Файл {input_file} не найден!")
        sys.exit(1)
    
    print_dataframe_info(df, "1. ЗАГРУЗКА ДАННЫХ И ФОРМИРОВАНИЕ DATAFRAME")
    
    # 2. Информация о колонках
    print("\n" + "=" * 60)
    print("2. ИНФОРМАЦИЯ О КОЛОНКАХ")
    print("=" * 60)
    print("DataFrame с оригинальными названиями колонок")
    print(df.head())
    print(f"Названия колонок: {list(df.columns)}")
    
    # 3. Добавление новой колонки
    print("\n" + "=" * 60)
    print("3. ДОБАВЛЕНИЕ КОЛОНКИ С ДИАПАЗОНОМ ЯРКОСТИ")
    print("=" * 60)
    
    print("Вычисление диапазона яркости для изображений...")
    df = add_brightness_range_column(df)
    
    print("\nDataFrame с новой колонкой:")
    print(df.head(10))
    print(f"\nСтатистика по колонке 'brightness_range':")
    print(df['brightness_range'].describe())
    
    # 4. Сортировка по добавленной колонке
    print("\n" + "=" * 60)
    print("4. СОРТИРОВКА ПО КОЛОНКЕ 'brightness_range'")
    print("=" * 60)
    
    sorted_df = sort_by_brightness_range(df)
    print("Первые 10 строк после сортировки (по возрастанию):")
    print(sorted_df[['relative_path', 'brightness_range']].head(10))
    
    # 5. Демонстрация фильтрации
    print("\n" + "=" * 60)
    print("5. ФИЛЬТРАЦИЯ ПО ДИАПАЗОНУ ЯРКОСТИ")
    print("=" * 60)
    
    high_contrast = filter_by_brightness_range(df, min_value=200)
    print(f"Изображения с высокой контрастностью (яркость >= 200): {len(high_contrast)}")
    
    # 6. Построение графика
    print("\n" + "=" * 60)
    print("6. ПОСТРОЕНИЕ ГРАФИКА ДЛЯ ОТСОРТИРОВАННЫХ ДАННЫХ")
    print("=" * 60)
    
    output_plot = create_brightness_plot(sorted_df)
    print(f"График сохранен в файл: {output_plot}")
    
    # 7. Сохранение DataFrame в файл
    print("\n" + "=" * 60)
    print("7. СОХРАНЕНИЕ DATAFRAME В ФАЙЛ")
    print("=" * 60)
    
    output_csv = 'result_dataframe.csv'
    df.to_csv(output_csv, index=False, encoding='utf-8')
    print(f"DataFrame сохранен в файл: {output_csv}")
    
    # Итоговая информация
    print("\n" + "=" * 60)
    print("ИТОГОВАЯ ИНФОРМАЦИЯ")
    print("=" * 60)
    print(f"Обработано изображений: {len(df)}")
    print(f"Диапазон яркости: от {df['brightness_range'].min():.2f} до {df['brightness_range'].max():.2f}")
    print(f"Средний диапазон яркости: {df['brightness_range'].mean():.2f}")
    
    print(f"\nСохраненные файлы:")
    print(f"- DataFrame: {output_csv}")
    print(f"- График: {output_plot}")


if __name__ == "__main__":
    main()