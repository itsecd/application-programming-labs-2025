import argparse
import os
from datetime import datetime
from downloader import ImageDownloader
from annotation_manager import AnnotationManager, ImageIterator

def main():
    """
    Главная функция приложения.
    Организует весь процесс: скачивание -> создание аннотации -> тестирование.
    """
    try:
        parser = argparse.ArgumentParser(description='Скачивание изображений обезьян за текущий год')
        parser.add_argument('--folder', type=str, required=True, 
                          help='Папка для сохранения изображений')
        parser.add_argument('--annotation', type=str, required=True,
                          help='CSV файл для сохранения аннотаций')
        args = parser.parse_args()

        # Определяем текущий год для информационных сообщений
        current_year = datetime.now().year
        print(f"=== Скачивание изображений обезьян за {current_year} год ===")
        print(f"Папка для изображений: {args.folder}")
        print(f"Файл аннотации: {args.annotation}")
        print("=" * 50)

        print("\n1. Скачиваем изображения...")
        downloader = ImageDownloader()
        downloaded_count = downloader.download_images(50, args.folder)

        print("\n2. Создаем аннотации...")
        annotation_manager = AnnotationManager()
        annotation_count = annotation_manager.create_annotation(args.folder, args.annotation)

        print("\n3. Тестируем итератор...")
        iterator = ImageIterator(annotation_file=args.annotation)
        print(f"Всего файлов доступно для обработки: {len(iterator)}")

        if len(iterator) > 0:
            print("Первые 3 файла из аннотации:")
            count = 0
            for path in iterator:
                print(f"  {os.path.basename(path)}")
                count += 1
                if count >= 3:
                    break
        else:
            print("Нет изображений для отображения")

        print("ОТЧЕТ")
        print(f"Скачано изображений за {current_year} год: {downloaded_count}")
        print(f"Записано в аннотацию: {annotation_count}")

        # Проверяем успешность выполнения
        if downloaded_count >= 50:
            print("УСПЕХ: Скачано 50+ изображений!")
        else:
            print(f"Скачано только {downloaded_count} изображений (цель: 50)")

        print("\nРабота программы завершена!")

    except KeyboardInterrupt:
        print("\n Программа прервана пользователем")
    except Exception as e:
        print(f"\n Критическая ошибка: {e}")


if __name__ == '__main__':
    main()