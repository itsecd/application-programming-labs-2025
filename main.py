"""
Основной модуль для запуска анализа аудиофайлов.
"""

from audio_analyzer import AudioAnalyzer
from visualization import AmplitudeVisualizer
from data_exporter import DataExporter


def main() -> None:
    """
    Основная функция для запуска анализа аудиофайлов.
    """
    try:
        # Инициализация анализатора
        analyzer = AudioAnalyzer('annotation.csv')
        
        # Загрузка и обработка данных
        analyzer.load_data()
        analyzer.add_amplitude_column()
        
        # Сортировка и фильтрация
        df_sorted = analyzer.sort_by_amplitude(ascending=False)
        df_filtered = analyzer.filter_by_amplitude(min_amplitude=0.1)
        
        # Визуализация
        AmplitudeVisualizer.create_amplitude_plot(df_sorted)
        AmplitudeVisualizer.create_amplitude_histogram(analyzer.df)
        
        # Экспорт данных
        DataExporter.export_to_csv(df_sorted)
        
        # Статистика
        stats = analyzer.get_amplitude_statistics()
        top_files = analyzer.get_top_files(5)
        DataExporter.print_statistics(stats, top_files)
        
    except Exception as e:
        print(f"Произошла ошибка: {e}")


if __name__ == '__main__':
    main()