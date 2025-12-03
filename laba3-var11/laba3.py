#!/usr/bin/env python3
"""
Модуль для обработки изображений.
Разделяет изображение на n равных частей и собирает их в случайном порядке.
"""

import argparse
import cv2
import numpy as np
import random
import matplotlib.pyplot as plt
import sys
import os
from typing import Tuple, List, Dict, Any, Optional


class ImageProcessor:
    """Класс для обработки изображений."""
    
    def __init__(self) -> None:
        """Инициализация обработчика изображений."""
        self.original_image: Optional[np.ndarray] = None
        self.processed_image: Optional[np.ndarray] = None
        self.image_parts: List[Dict[str, Any]] = []
        self.shuffled_parts: List[Dict[str, Any]] = []
    
    def load_image(self, image_path: str) -> np.ndarray:
        """
        Загружает изображение из файла.
        
        Args:
            image_path: Путь к файлу изображения
            
        Returns:
            Загруженное изображение в виде numpy массива
            
        Raises:
            FileNotFoundError: Если файл не найден
            ValueError: Если не удалось загрузить изображение
        """
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Файл {image_path} не найден")
        
        image = cv2.imread(image_path)
        if image is None:
            raise ValueError(f"Не удалось загрузить изображение {image_path}")
        
        self.original_image = image
        return image
    
    def get_image_info(self, image: np.ndarray) -> Dict[str, Any]:
        """
        Возвращает информацию об изображении.
        
        Args:
            image: Изображение в виде numpy массива
            
        Returns:
            Словарь с информацией об изображении
        """
        height, width = image.shape[:2]
        channels = image.shape[2] if len(image.shape) == 3 else 1
        
        return {
            'width': width,
            'height': height,
            'channels': channels,
            'dtype': str(image.dtype)
        }
    
    def validate_parameters(self, image: np.ndarray, n: int) -> None:
        """
        Проверяет параметры для обработки изображения.
        
        Args:
            image: Изображение для проверки
            n: Количество частей
            
        Raises:
            ValueError: Если параметры некорректны
        """
        if n <= 0:
            raise ValueError("Количество частей должно быть положительным числом")
        
        height, width = image.shape[:2]
        if n > min(height, width):
            raise ValueError(
                f"Количество частей ({n}) превышает размер изображения "
                f"({width}x{height})"
            )
    
    def split_image(self, image: np.ndarray, n: int) -> List[Dict[str, Any]]:
        """
        Разделяет изображение на n x n равных частей.
        
        Args:
            image: Исходное изображение
            n: Количество частей по горизонтали и вертикали
            
        Returns:
            Список частей изображения с метаданными
        """
        height, width = image.shape[:2]
        
        # Вычисляем размер каждой части
        part_height = height // n
        part_width = width // n
        
        # Обрезаем изображение до размеров, кратных n
        new_height = part_height * n
        new_width = part_width * n
        cropped_image = image[:new_height, :new_width]
        
        parts = []
        
        for i in range(n):
            for j in range(n):
                part = cropped_image[i * part_height:(i + 1) * part_height,
                                     j * part_width:(j + 1) * part_width]
                
                parts.append({
                    'data': part.copy(),
                    'original_position': (i, j),
                    'size': (part_height, part_width)
                })
        
        self.image_parts = parts
        return parts
    
    def shuffle_parts(self, parts: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Перемешивает части изображения.
        
        Args:
            parts: Список частей изображения
            
        Returns:
            Перемешанный список частей
        """
        shuffled = parts.copy()
        random.shuffle(shuffled)
        self.shuffled_parts = shuffled
        return shuffled
    
    def reassemble_image(self, shuffled_parts: List[Dict[str, Any]], n: int) -> np.ndarray:
        """
        Собирает изображение из перемешанных частей.
        
        Args:
            shuffled_parts: Перемешанные части изображения
            n: Количество частей по горизонтали и вертикали
            
        Returns:
            Собранное изображение
        """
        if not shuffled_parts:
            raise ValueError("Нет частей для сборки")
        
        part_height, part_width = shuffled_parts[0]['size']
        channels = shuffled_parts[0]['data'].shape[2] if len(shuffled_parts[0]['data'].shape) == 3 else 1
        
        # Создаем пустое изображение для сборки
        if channels == 1:
            result = np.zeros((part_height * n, part_width * n), dtype=np.uint8)
        else:
            result = np.zeros((part_height * n, part_width * n, channels), dtype=np.uint8)
        
        # Собираем изображение
        for idx, part_info in enumerate(shuffled_parts):
            i = idx // n  # Новая строка
            j = idx % n   # Новый столбец
            
            result[i * part_height:(i + 1) * part_height,
                   j * part_width:(j + 1) * part_width] = part_info['data']
        
        self.processed_image = result
        return result
    
    def save_image(self, image: np.ndarray, output_path: str) -> bool:
        """
        Сохраняет изображение в файл.
        
        Args:
            image: Изображение для сохранения
            output_path: Путь для сохранения
            
        Returns:
            True если сохранение успешно, False в противном случае
            
        Raises:
            ValueError: Если изображение пустое
        """
        if image is None or image.size == 0:
            raise ValueError("Изображение для сохранения пустое")
        
        return cv2.imwrite(output_path, image)
    
    def process_image(self, input_path: str, output_path: str, n: int) -> bool:
        """
        Основной метод обработки изображения.
        
        Args:
            input_path: Путь к исходному изображению
            output_path: Путь для сохранения результата
            n: Количество частей по горизонтали и вертикали
            
        Returns:
            True если обработка успешна, False в противном случае
        """
        try:
            # Загрузка изображения
            image = self.load_image(input_path)
            
            # Получение информации об изображении
            info = self.get_image_info(image)
            print(f"Загружено изображение: {info['width']}x{info['height']}, "
                  f"каналы: {info['channels']}")
            
            # Проверка параметров
            self.validate_parameters(image, n)
            
            # Разделение изображения
            print(f"Разделение изображения на {n}x{n} = {n*n} частей...")
            parts = self.split_image(image, n)
            
            # Перемешивание частей
            print("Перемешивание частей...")
            shuffled_parts = self.shuffle_parts(parts)
            
            # Сборка изображения
            print("Сборка изображения из перемешанных частей...")
            result = self.reassemble_image(shuffled_parts, n)
            
            # Сохранение результата
            if self.save_image(result, output_path):
                print(f"Результат сохранен в: {output_path}")
                return True
            else:
                print(f"Ошибка при сохранении в: {output_path}")
                return False
                
        except Exception as e:
            print(f"Ошибка при обработке изображения: {e}")
            return False


def visualize_results(processor: ImageProcessor, n: int, figsize: Tuple[int, int] = (15, 8)) -> None:
    """
    Визуализирует результаты обработки изображения.
    
    Args:
        processor: Объект ImageProcessor с обработанным изображением
        n: Количество частей по горизонтали и вертикали
        figsize: Размер фигуры для отображения
    """
    if processor.original_image is None or processor.processed_image is None:
        print("Нет данных для визуализации")
        return
    
    # Преобразование BGR в RGB для отображения
    if len(processor.original_image.shape) == 3:
        original_rgb = cv2.cvtColor(processor.original_image, cv2.COLOR_BGR2RGB)
        processed_rgb = cv2.cvtColor(processor.processed_image, cv2.COLOR_BGR2RGB)
    else:
        original_rgb = processor.original_image
        processed_rgb = processor.processed_image
    
    # Создание фигуры
    fig, axes = plt.subplots(2, 3, figsize=figsize)
    
    # 1. Исходное изображение
    axes[0, 0].imshow(original_rgb)
    axes[0, 0].set_title('Исходное изображение')
    axes[0, 0].axis('off')
    
    # 2. Обработанное изображение
    axes[0, 1].imshow(processed_rgb)
    axes[0, 1].set_title(f'Перемешанное ({n}x{n})')
    axes[0, 1].axis('off')
    
    # 3. Сетка на исходном изображении
    grid_img = original_rgb.copy()
    height, width = original_rgb.shape[:2]
    part_height = height // n
    part_width = width // n
    
    # Рисование линий сетки
    for i in range(1, n):
        cv2.line(grid_img, (0, i * part_height), (width, i * part_height), (255, 0, 0), 2)
        cv2.line(grid_img, (i * part_width, 0), (i * part_width, height), (255, 0, 0), 2)
    
    axes[0, 2].imshow(grid_img)
    axes[0, 2].set_title(f'Сетка {n}x{n}')
    axes[0, 2].axis('off')
    
    # 4-6. Примеры отдельных частей
    num_examples = min(3, len(processor.image_parts))
    for i in range(num_examples):
        part = processor.image_parts[i]['data']
        if len(part.shape) == 3:
            part_rgb = cv2.cvtColor(part, cv2.COLOR_BGR2RGB)
        else:
            part_rgb = part
        
        axes[1, i].imshow(part_rgb)
        axes[1, i].set_title(f'Часть {i+1}')
        axes[1, i].axis('off')
    
    # Скрытие пустых subplots
    for i in range(num_examples, 3):
        axes[1, i].axis('off')
    
    plt.tight_layout()
    plt.show()


def parse_arguments() -> argparse.Namespace:
    """
    Парсит аргументы командной строки.
    
    Returns:
        Объект с аргументами командной строки
    """
    parser = argparse.ArgumentParser(
        description='Разделение изображения на n равных частей и случайная перестановка',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Примеры использования:
  python image_processor.py input.jpg output.jpg 3
  python image_processor.py photo.png result.png 4
        """
    )
    
    parser.add_argument(
        'input',
        type=str,
        help='Путь к исходному изображению'
    )
    
    parser.add_argument(
        'output',
        type=str,
        help='Путь для сохранения результата'
    )
    
    parser.add_argument(
        'n',
        type=int,
        help='Количество частей по горизонтали и вертикали (n x n)'
    )
    
    return parser.parse_args()


def validate_arguments(args: argparse.Namespace) -> bool:
    """
    Проверяет корректность аргументов командной строки.
    
    Args:
        args: Аргументы командной строки
        
    Returns:
        True если аргументы корректны, False в противном случае
    """
    try:
        if not os.path.exists(args.input):
            print(f"Ошибка: файл {args.input} не найден")
            return False
        
        if args.n <= 0:
            print("Ошибка: количество частей должно быть положительным числом")
            return False
        
        return True
        
    except Exception as e:
        print(f"Ошибка при проверке аргументов: {e}")
        return False


def main() -> None:
    """Основная функция программы."""
    try:
        # Парсинг аргументов командной строки
        args = parse_arguments()
        
        # Проверка аргументов
        if not validate_arguments(args):
            sys.exit(1)
        
        print("=" * 60)
        print(f"Обработка изображения: {args.input}")
        print(f"Выходной файл: {args.output}")
        print(f"Количество частей: {args.n}x{args.n} = {args.n * args.n}")
        print("=" * 60)
        
        # Создание обработчика изображений
        processor = ImageProcessor()
        
        # Обработка изображения
        success = processor.process_image(args.input, args.output, args.n)
        
        if success:
            print("\nОбработка завершена успешно!")
            
            # Визуализация результатов
            print("\nВизуализация результатов...")
            visualize_results(processor, args.n)
            
        else:
            print("\nОбработка завершена с ошибками")
            sys.exit(1)
            
    except KeyboardInterrupt:
        print("\n\nПрограмма прервана пользователем")
        sys.exit(0)
    except Exception as e:
        print(f"\nНепредвиденная ошибка: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
