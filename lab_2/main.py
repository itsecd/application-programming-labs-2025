import argparse
import sys
from pathlib import Path
from downloader import download_images, _create_annotation
from image_iterator import ImageIterator


def main() -> None:
    """Основная функция для выполнения скрипта.
    
    Скачивает изображения по заданному запросу, создает аннотационный CSV-файл
    и демонстрирует работу итератора по изображениям.
    
    Raises:
        SystemExit: Завершение работы с кодом ошибки при возникновении исключения
    """
    parser = argparse.ArgumentParser(
        description='Скачивание изображений и создание аннотации'
    )
    parser.add_argument(
        '--output_dir',
        type=str,
        required=True,
        help='Путь к папке для сохранения изображений'
    )
    parser.add_argument(
        '--annotation_file',
        type=str,
        required=True,
        help='Путь к файлу аннотации CSV'
    )
    parser.add_argument(
        '--num_threads',
        type=int,
        required=True,
        help='Количество потоков для скачивания'
    )
    
    try:
        args = parser.parse_args()
        
        _validate_arguments(args)
        
        '''download_images(
            output_dir=args.output_dir,
            annotation_file=args.annotation_file,
            num_threads=args.num_threads
        )'''

        _create_annotation(Path(args.output_dir), Path(args.annotation_file))

        print("\nДемонстрация работы итератора:")
        image_iterator = ImageIterator(args.annotation_file)
        for i, image_path in enumerate(image_iterator, 1):
            print(f"{i}: {image_path}")
            
    except argparse.ArgumentError as e:
        print(f"Ошибка в аргументах командной строки: {e}")
        print("Используйте --help для получения справки")
        sys.exit(1)
    except ValueError as e:
        print(f"Ошибка значения: {e}")
        sys.exit(1)
    except FileNotFoundError as e:
        print(f"Файл или директория не найдена: {e}")
        sys.exit(1)
    except PermissionError as e:
        print(f"Ошибка доступа: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nПрограмма прервана пользователем")
        sys.exit(1)
    


def _validate_arguments(args: argparse.Namespace) -> None:
    """Проверяет корректность аргументов командной строки.
    
    Args:
        args: Аргументы командной строки
        
    Raises:
        ValueError: Если аргументы не прошли валидацию
    """
    if args.num_threads <= 0:
        raise ValueError("Количество потоков должно быть положительным числом")
    
    if args.num_threads > 10:
        print("Предупреждение: использование более 10 потоков может привести к блокировке")
    
    output_dir = Path(args.output_dir)
    if output_dir.exists() and not output_dir.is_dir():
        raise ValueError(f"Выходная директория {args.output_dir} уже существует как файл")
    
    annotation_file = Path(args.annotation_file)
    if annotation_file.exists() and not annotation_file.is_file():
        raise ValueError(f"Файл аннотации {args.annotation_file} уже существует как директория")
    
    if annotation_file.suffix.lower() != '.csv':
        print("Предупреждение: рекомендуется использовать расширение .csv для файла аннотации")


if __name__ == "__main__":
    main()