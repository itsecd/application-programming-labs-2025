"""Основной модуль программы для анализа аудиоданных."""
from pathlib import Path

import pandas as pd

import config
from audio_processor import AudioProcessor
from plot_generator import PlotGenerator


def main() -> None:
    """
    Основная функция программы.
    Выполняет полный анализ аудиоданных: загрузка аннотации, создание DataFrame,
    добавление колонки с диапазонами амплитуды, сортировка, фильтрация, 
    построение графиков и сохранение результатов.
    """
    try:
        if not config.ANNOTATION_FILE.exists():
            print(f"Файл аннотации не найден: {config.ANNOTATION_FILE}")
            return
        
        processor = AudioProcessor(config.ANNOTATION_FILE, config.DOWNLOAD_DIR)
        processor.process_audio_data()
        
        if processor.df is None or processor.df.empty:
            print("Не удалось обработать аудиоданные")
            return
        
        df = processor.df
        plotter = PlotGenerator()
        
        # 1. DataFrame с путями 
        paths_df = df[['absolute_path', 'relative_path']].copy()
        print("1. DataFrame с путями к файлам (абсолютный и относительный пути):")
        print(paths_df.head())
        
        # 2. Добавление колонки для гистограммы 
        paths_df['amplitude_range_bin'] = df['amplitude_range_bin']
        print("\n2. DataFrame с добавленной колонкой диапазонов амплитуды (range=max-min):")
        print(paths_df[['absolute_path', 'relative_path', 'amplitude_range_bin']].head())
        
        # 3. Сортировка по амплитуде 
        sorted_df = processor.sort_by_amplitude_range(df, ascending=True)
        sorted_paths = sorted_df[['absolute_path', 'relative_path', 'amplitude_range_bin']]
        print("\n3. Отсортированные данные по диапазону амплитуды (по возрастанию):")
        print(sorted_paths.head())
        
        # 4. Фильтрация по амплитуде 
        filtered_df = processor.filter_by_amplitude_range(df, 0.5, 1.0)
        filtered_paths = filtered_df[['absolute_path', 'relative_path', 'amplitude_range_bin']]
        print(f"\n4. Фильтрация по диапазону амплитуды 0.5-1.0: найдено {len(filtered_paths)} файлов")
        print(filtered_paths.head())
        
        # 5. Создание графиков 
        plotter.create_amplitude_histogram(df, config.OUTPUT_PLOT_FILE)
        sorted_plot_file = Path("sorted_amplitudes.png")
        plotter.create_sorted_amplitude_plot(sorted_df, sorted_plot_file)
        print(f"\n5. Графики созданы: {config.OUTPUT_PLOT_FILE} (гистограмма), {sorted_plot_file} (отсортированные значения)")
        
        # 6. Сохранение файлов 
        paths_df.to_csv(config.OUTPUT_DF_FILE, index=False, sep=';', encoding='utf-8-sig')
        print(f"6. DataFrame сохранен: {config.OUTPUT_DF_FILE} ")
        
    except Exception as e:
        print(f"Ошибка: {e}")

if __name__ == "__main__":
    main()
