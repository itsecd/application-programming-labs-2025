"""Основной модуль для третьей лабораторной работы."""
import argparse
import os
from dataframe_manager import DataFrameManager
from plot_generator import PlotGenerator

def parse_args() -> argparse.Namespace:
    """
    Парсит аргументы командной строки.

    Returns:
        Объект с аргументами
    """
    parser = argparse.ArgumentParser(
        description="Анализ аудиофайлов и создание DataFrame с графиками"
    )
    parser.add_argument(
        "--annotation",
        required=True,
        help="Путь к CSV файлу аннотации из второй лабораторной работы"
    )
    parser.add_argument(
        "--output_df",
        default="results/audio_analysis.csv",
        help="Путь для сохранения результирующего DataFrame"
    )
    parser.add_argument(
        "--output_plot",
        default="results/duration_plot.png", 
        help="Путь для сохранения графика"
    )
    return parser.parse_args()


def print_dataframe_info(info: dict) -> None:
    """
    Выводит информацию о DataFrame в удобочитаемом формате.

    Args:
        info: Словарь с информацией о DataFrame
    """
    print("\n" + "="*50)
    print("ИНФОРМАЦИЯ О DATAFRAME")
    print("="*50)
    print(f"Количество файлов: {info['total_files']}")
    print(f"Колонки: {info['columns']}")
    
    if 'total_duration' in info:
        print(f"Общая длительность всех файлов: {info['total_duration']} секунд")
        print(f"Средняя длительность: {info['average_duration']} секунд")
        print(f"Максимальная длительность: {info['max_duration']} секунд") 
        print(f"Минимальная длительность: {info['min_duration']} секунд")
    print("="*50 + "\n")


def main() -> None:
    """Основная функция программы."""
    try:
        args = parse_args()
        
        df_manager = DataFrameManager()
        
        
        print("\n1. Создание DataFrame из аннотации...")
        df = df_manager.create_dataframe_from_annotation(args.annotation)
        print(f"DataFrame создан. Колонки: {list(df.columns)}")
        
        print("\n2. Добавление колонки с длительностью...")
        df_manager.add_duration_column()
        print("Колонка с длительностью успешно добавлена")
        
        info = df_manager.get_dataframe_info()
        print_dataframe_info(info)
        
        print("\n3. Сортировка данных по длительности...")
        sorted_df = df_manager.sort_by_duration(ascending=True)
        print("Данные отсортированы по длительности (по возрастанию)")
        
        print("\n4. Демонстрация фильтрации...")
        filtered_df = df_manager.filter_by_duration(min_duration=2.0, max_duration=10.0)
        print(f"Найдено {len(filtered_df)} файлов длительностью от 2 до 10 секунд")
        
        print("\n5. Создание графика для отсортированных данных...")
        plot_generator = PlotGenerator()
        
        plot_generator.create_duration_plot(sorted_df, args.output_plot)
        print(f"График распределения длительности сохранен в: {args.output_plot}")
        
        print("\n6. Сохранение результатов...")
        df_manager.save_dataframe(args.output_df)
        print(f"DataFrame сохранен в: {args.output_df}")
        
        
    except Exception as e:
        print(f"Критическая ошибка в работе программы: {e}")
        raise


if __name__ == "__main__":
    main()