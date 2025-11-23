"""Основной модуль программы."""
import os
from image_analyzer import ImageAnalyzer
from data_processor import DataProcessor
from visualization import DataVisualizer


def main():
    """Основная функция программы."""
    annotation_file = r"C:\Users\gayvo\OneDrive\Desktop\pp\lab2\annotation.csv"
    images_folder = r"C:\Users\gayvo\OneDrive\Desktop\pp\lab2\bird_images"

    analyzer = ImageAnalyzer()
    processor = DataProcessor()
    visualizer = DataVisualizer()

    try:
        
        df = processor.load_annotation_data(annotation_file)
        
        image_paths = df['Абсолютный_путь'].tolist()
        brightness_values = analyzer.process_images_brightness(image_paths)
        df_with_brightness = processor.add_brightness_column(brightness_values)
        stats = processor.get_statistics()
        sorted_df = processor.sort_by_brightness(ascending=False)
        filtered_df = processor.filter_by_brightness(min_brightness=150)
        visualizer.plot_brightness_distribution(
            sorted_df,
            'bird_brightness_plot.png'
        )

        processor.save_dataframe('bird_images_analysis.csv')

        print("Анализ завершен успешно!")
        

    except FileNotFoundError as e:
        print(f"Ошибка: Файл не найден - {e}")
    except Exception as e:
        print(f"Произошла ошибка: {e}")


if __name__ == "__main__":
    main()