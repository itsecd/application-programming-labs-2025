import argparse
import sys
from pathlib import Path
from typing import List

from downloader import download_images_simple
from annotation import create_annotation_csv


def main() -> None:
    """Основная функция"""
    parser = argparse.ArgumentParser(
        description='Скачивание изображений и создание аннотации'
    )
    
    parser.add_argument('--output_dir', '-o', required=True, 
                       help='Путь к папке для сохранения изображений')
    parser.add_argument('--annotation_file', '-a', required=True,
                       help='Путь к файлу аннотации (CSV)')
    parser.add_argument('--keywords', '-k', nargs='+', required=True,
                       help='Ключевые слова для поиска изображений')
    parser.add_argument('--num_per_keyword', '-n', type=int, required=True,
                       help='Количество изображений для каждого ключевого слова')
    
    args = parser.parse_args()
    
    # Проверяем аргументы
    if args.num_per_keyword <= 0:
        print("Ошибка: количество изображений должно быть положительным числом")
        sys.exit(1)
    
    if len(args.keywords) == 0:
        print("Ошибка: необходимо указать хотя бы одно ключевое слово")
        sys.exit(1)
    
    total_images = len(args.keywords) * args.num_per_keyword
    print(f"Всего будет скачано: {total_images} изображений")
    
    if total_images < 50:
        print(f"  Предупреждение: количество изображений ({total_images}) меньше 50")
        response = input("Продолжить? (y/n): ").lower()
        if response != 'y':
            print("Отмена выполнения")
            sys.exit(0)
    
    # Скачиваем изображения
    downloaded_files = download_images_simple(
        args.keywords, 
        args.num_per_keyword, 
        args.output_dir
    )
    
    if not downloaded_files:
        print(" Не удалось скачать ни одного изображения")
        print("Возможные причины:")
        print("1. Проблемы с интернет-соединением")
        print("2. Антивирус блокирует скачивание") 
        print("3. Ключевые слова не найдены")
        print("4. Проблемы с библиотекой icrawler")
        sys.exit(1)
    
    # Создаем аннотацию
    create_annotation_csv(downloaded_files, args.output_dir, args.annotation_file)
    
    print(f"\n Успешно завершено!")
    print(f" Изображения: {args.output_dir}")
    print(f" Аннотация: {args.annotation_file}")
    print(f"  Скачано: {len(downloaded_files)} изображений")


if __name__ == "__main__":
    main()