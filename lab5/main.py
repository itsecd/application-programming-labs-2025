import argparse
from pathlib import Path

from date_parser import parse_date_ranges
from image_distributor import ImageDistributor
from image_downloader import BearImageDownloader
from annotation_creator import create_annotation_csv
from image_iterator import ImageIterator


def main() -> None:
    """Основная функция для запуска процесса скачивания изображений."""
    parser = argparse.ArgumentParser(
        description='Скачивание 50-1000 изображений медведей по диапазонам дат со случайным распределением'
    )
    parser.add_argument(
        '--output_dir', 
        required=True,
        help='Папка для сохранения изображений'
    )
    parser.add_argument(
        '--annotation_file', 
        required=True, 
        help='CSV файл аннотации'
    )
    parser.add_argument(
        '--date_ranges', 
        required=True,
        help='Диапазоны дат через запятую: start1-end1,start2-end2'
    )
    
    args = parser.parse_args()
    
    try:
        """Парсинг диапазонов дат"""
        date_ranges = parse_date_ranges(args.date_ranges)
        print(f"Обработано диапазонов дат: {len(date_ranges)}")
        for i, (start, end) in enumerate(date_ranges):
            print(f"  Диапазон {i+1}: {start} - {end}")
    except ValueError as e:
        print(f"Ошибка в формате дат: {e}")
        return
    
    try:
        """Распределение изображений"""
        distributor = ImageDistributor()
        total_images, images_per_range = distributor.distribute_with_user_input(len(date_ranges))
        
        """Скачивание изображений"""
        downloader = BearImageDownloader()
        image_paths = downloader.download_images(date_ranges, images_per_range, args.output_dir)
        
        """Создание аннотации"""
        create_annotation_csv(image_paths, args.annotation_file, args.output_dir)
        
        """Демонстрация результатов"""
        _display_results(image_paths, args.annotation_file)
    except Exception as e:
        print(f"Произошла ошибка при выполнении основной логики: {e}")


def _display_results(image_paths: list, annotation_file: str) -> None:
    """Отображает результаты работы программы."""
    print(f"\nРЕЗУЛЬТАТ: Скачано {len(image_paths)} изображений")
    
    if len(image_paths) < 50:
        print("ВНИМАНИЕ: Не удалось достичь минимума в 50 изображений")
        print("Возможные причины:")
        print("1. Ограничения поисковика")
        print("2. Мало результатов по данным диапазонам дат")
        print("3. Попробуйте другие диапазоны дат")
    else:
        print("УСПЕХ: Достигнуто требуемое количество изображений")
    
    print(f"\nДемонстрация итератора:")
    iterator = ImageIterator(annotation_file)
    print(f"Всего путей в итераторе: {len(iterator.paths)}")
    
    print("Первые 5 файлов:")
    for i, path in enumerate(iterator):
        if i < 5:
            print(f"  {Path(path).name}")
        else:
            break


if __name__ == '__main__':
    main()