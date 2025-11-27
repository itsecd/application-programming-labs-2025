import argparse
import sys
import matplotlib.pyplot as plt
from brightness_processing import (
    load_image_paths, 
    process_brightness, 
    sort_by_brightness, 
    filter_by_brightness
)
from graphics import (
    create_graph,
    save_dataframe_to_csv, 
    save_plot_to_file
)

def parse_arguments():
    """Парсинг аргументов командной строки."""
    parser = argparse.ArgumentParser(description='Анализ диапазона яркости изображений')
    parser.add_argument('--csv', '-c', type=str, required=True, help='Путь к CSV файлу с аннотациями')
    return parser.parse_args()


def main():
    """Основная функция выполнения задания."""
    try:
        
        args = parse_arguments()
        print(f"CSV файл: {args.csv}")
        
        image_paths = load_image_paths(args.csv)  
        
        if not image_paths:
            sys.exit(1)
        
        df = process_brightness(image_paths, args.csv) 
        if df.empty:
            print("Нет данных для анализа")
            sys.exit(1)
        
        sorted_df = sort_by_brightness(df)
              
        filtered_df = filter_by_brightness(df, min_range=100)
        
        fig = create_graph(df)
        save_dataframe_to_csv(df)
        save_plot_to_file(fig, 'brightness_histogram.png')
        plt.show()
       
        
    except Exception as e:
        print(f"Ошибка: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()