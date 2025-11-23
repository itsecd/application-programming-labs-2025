import argparse
import os

from dataframe_manager import DataFrameManager
from image_analyzer import ImageAnalyzer
from visualizer import Visualizer

def main():
    """Главная функция приложения."""
    try:
        parser = argparse.ArgumentParser(
            description='Анализ яркости изображений и создание графиков'
        )
        parser.add_argument(
            '--annotation', type=str, required=True,
            help='CSV файл с аннотациями изображений'
        )
        parser.add_argument(
            '--output_df', type=str, required=True,
            help='Файл для сохранения обогащенного DataFrame'
        )
        parser.add_argument(
            '--output_plot', type=str, required=True,
            help='Файл для сохранения графика распределения'
        )
        parser.add_argument(
            '--ranges', type=str, default='0-85,86-170,171-255',
            help='Диапазоны яркости в формате "0-50,51-150,151-255"'
        )
        args = parser.parse_args()

        # Парсинг диапазонов
        brightness_ranges = []
        try:
            range_parts = args.ranges.split(',')
            for range_part in range_parts:
                low, high = map(int, range_part.split('-'))
                brightness_ranges.append((low, high, f"{low}-{high}"))
        except Exception as e:
            print(f"Ошибка парсинга диапазонов: {e}")
            print("Используются диапазоны по умолчанию: 0-85,86-170,171-255")
            brightness_ranges = [(0, 85, "0-85"), (86, 170, "86-170"), (171, 255, "171-255")]

        print("=== Анализ яркости изображений ===")
        print(f"Файл аннотации: {args.annotation}")
        print(f"Выходной DataFrame: {args.output_df}")
        print(f"Выходной график: {args.output_plot}")
        print(f"Диапазоны яркости: {[r[2] for r in brightness_ranges]}")
        print("=" * 50)

        print("\n1. Создаем DataFrame из аннотации...")
        df_manager = DataFrameManager()
        df = df_manager.create_from_annotation(args.annotation)

        if len(df) == 0:
            print("Ошибка: в аннотации нет данных!")
            return

        print("\n2. Поиск существующих изображений...")
        valid_image_paths = df_manager.get_valid_image_paths()

        if len(valid_image_paths) == 0:
            print("Ошибка: не найдено ни одного существующего изображения!")
            print("Убедитесь, что:")
            print(" - Папка с изображениями существует")
            print(" - Файлы изображений присутствуют в папке")
            print(" - Относительные пути в аннотации верны")
            return

        print("\n3. Анализируем яркость изображений...")
        analyzer = ImageAnalyzer(brightness_ranges)
        visualizer = Visualizer(brightness_ranges)

        brightness_data = []

        for idx, image_path in enumerate(valid_image_paths):
            if idx % 5 == 0 and idx > 0:
                print(f"  Обработано {idx}/{len(valid_image_paths)} изображений...")

            stats = analyzer.get_brightness_stats(image_path)
            brightness_data.append(stats)

        print(f"  Успешно проанализировано {len(brightness_data)} изображений")

        print("\n4. Добавляем данные о яркости в DataFrame...")
        df_manager.add_brightness_columns(valid_image_paths, brightness_data)
        df_manager.print_brightness_stats()

        print("\n5. Демонстрация функций сортировки и фильтрации...")

        df_sorted = df_manager.sort_by_brightness(brightness_ranges)

        # Фильтрация по диапазонам
        for brightness_range in [r[2] for r in brightness_ranges]:
            filtered_df = df_manager.filter_by_brightness(brightness_range)
            if len(filtered_df) > 0:
                first_file = filtered_df.iloc[0]
                filename = os.path.basename(first_file['relative_path'])
                print(f"  Пример с диапазоном '{brightness_range}': {filename}")

        print("\n6. Создаем графики...")

        # Гистограммы по каналам
        visualizer.plot_channel_histograms(df_manager.df, "channel_histograms.png")

        # Распределение по диапазонам яркости
        visualizer.plot_brightness_distribution(df_sorted, args.output_plot)

        print("\n7. Сохраняем результаты...")
        df_manager.save_to_csv(args.output_df)

        print("\n" + "=" * 50)
        print("ОТЧЕТ:")
        print(f"Всего записей в аннотации: {len(df)}")
        print(f"Найдено изображений: {len(valid_image_paths)}")
        print(f"Проанализировано: {len(brightness_data)}")
        print(f"DataFrame сохранен в: {args.output_df}")
        print(f"График распределения сохранен в: {args.output_plot}")
        print(f"Гистограммы каналов сохранены в: channel_histograms.png")
        print(f"Использованные диапазоны: {[r[2] for r in brightness_ranges]}")

        print("\nРабота программы завершена успешно!")

    except KeyboardInterrupt:
        print("\nПрограмма прервана пользователем")
    except Exception as e:
        print(f"\nКритическая ошибка: {e}")
        raise  


if __name__ == '__main__':
    main()