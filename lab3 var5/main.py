from image_processor import process_image, ImageProcessor
import argparse
import sys


def parse_arguments() -> argparse.Namespace:
    """
    Парсер аргументов командной строки.

    :return: объект Namespace с аргументами
    """
    parser = argparse.ArgumentParser(description="Инверсия цветов изображения.")
    parser.add_argument("input_file", help="Путь к исходному изображению.")
    parser.add_argument("output_file", help="Путь для сохранения обработанного изображения.")
    return parser.parse_args()


def main():
    """
    Основная функция программы с обработкой исключений и выводом сообщений.
    """
    try:
        args = parse_arguments()
        
        # Обрабатываем изображение
        success, message = process_image(args.input_file, args.output_file)
        
        if success:
            print("Обработка изображения завершена успешно!")
            print(message)  # Информация о размере изображения
            print(f"Обработанное изображение сохранено в '{args.output_file}'.")
        else:
            print(f"Ошибка при обработке изображения: {message}")
            sys.exit(1)
            
    except FileNotFoundError:
        print("Ошибка: один из указанных файлов не найден.")
        sys.exit(1)
    except PermissionError:
        print("Ошибка: недостаточно прав для чтения/записи файлов.")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nПрограмма прервана пользователем.")
        sys.exit(1)
    except Exception as e:
        print(f"Непредвиденная ошибка: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()