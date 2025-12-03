#!/usr/bin/env python3
"""
Модуль для создания пазлов из изображений.
Разделяет изображение на N×N частей и собирает в случайном порядке.
"""

import sys
import os
import random
from typing import Tuple, List
import numpy as np
import cv2
import matplotlib.pyplot as plt


class ImagePuzzle:
    """Создатель пазлов из изображений."""
    
    def __init__(self) -> None:
        """Инициализация создателя пазлов."""
        self.original = None
        self.puzzle = None
        self.tile_size = (0, 0)
        self.tile_count = 0
    
    def load_image(self, filepath: str) -> np.ndarray:
        """Загружает изображение из файла."""
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Файл не найден: {filepath}")
        
        img = cv2.imread(filepath)
        if img is None:
            raise ValueError(f"Не удалось загрузить изображение: {filepath}")
        
        self.original = img
        width, height = img.shape[1], img.shape[0]
        channels = img.shape[2]
        print(f"Загружено изображение: {width}x{height} пикселей, {channels} каналов")
        return img
    
    def split_image(self, n: int) -> List[np.ndarray]:
        """Разрезает изображение на n x n частей."""
        height, width = self.original.shape[:2]
        tile_h = height // n
        tile_w = width // n
        
        self.tile_size = (tile_h, tile_w)
        self.tile_count = n * n
        
        tiles = []
        for i in range(n):
            for j in range(n):
                tile = self.original[
                    i * tile_h:(i + 1) * tile_h,
                    j * tile_w:(j + 1) * tile_w
                ]
                tiles.append(tile)
        
        print(f"Создано {self.tile_count} частей размером {tile_w}x{tile_h}")
        return tiles
    
    def shuffle_and_build(self, tiles: List[np.ndarray], n: int) -> np.ndarray:
        """Перемешивает и собирает части в новое изображение."""
        tile_h, tile_w = self.tile_size
        height, width = self.original.shape[:2]
        
        shuffled = tiles.copy()
        random.shuffle(shuffled)
        
        result = np.zeros_like(self.original)
        idx = 0
        
        for i in range(n):
            for j in range(n):
                result[
                    i * tile_h:(i + 1) * tile_h,
                    j * tile_w:(j + 1) * tile_w
                ] = shuffled[idx]
                idx += 1
        
        self.puzzle = result
        return result
    
    def save_result(self, output_dir: str, filename: str = "puzzle_result.jpg") -> str:
        """Сохраняет результат в директорию."""
        output_path = os.path.join(output_dir, filename)
        
        if not os.path.exists(output_dir):
            os.makedirs(output_dir, exist_ok=True)
            print(f"Создана директория: {output_dir}")
        
        if cv2.imwrite(output_path, self.puzzle):
            print(f"Изображение сохранено: {output_path}")
            return output_path
        else:
            raise IOError(f"Не удалось сохранить: {output_path}")
    
    def show_comparison(self) -> None:
        """Показывает сравнение исходного и результата."""
        if self.original is None or self.puzzle is None:
            raise ValueError("Нет данных для отображения")
        
        original_rgb = cv2.cvtColor(self.original, cv2.COLOR_BGR2RGB)
        puzzle_rgb = cv2.cvtColor(self.puzzle, cv2.COLOR_BGR2RGB)
        
        fig, axes = plt.subplots(1, 2, figsize=(14, 6))
        
        axes[0].imshow(original_rgb)
        axes[0].set_title('Оригинальное изображение', fontsize=14)
        axes[0].axis('off')
        
        axes[1].imshow(puzzle_rgb)
        axes[1].set_title(f'Пазл ({int(np.sqrt(self.tile_count))}×{int(np.sqrt(self.tile_count))})', fontsize=14)
        axes[1].axis('off')
        
        plt.suptitle('Сравнение: оригинал и пазл', fontsize=16)
        plt.tight_layout()
        plt.show()


def get_n_from_user() -> int:
    """Запрашивает у пользователя количество делений."""
    while True:
        try:
            n = int(input("Введите количество частей для деления (например, 3 для 3×3): "))
            if n < 2:
                print("Минимум 2 части. Попробуйте снова.")
            elif n > 20:
                print("Максимум 20 частей. Попробуйте снова.")
            else:
                return n
        except ValueError:
            print("Введите целое число.")


def show_summary(input_path: str, output_dir: str, n: int) -> None:
    """Показывает сводку параметров."""
    print("\nПараметры обработки:")
    print(f"  Исходный файл: {input_path}")
    print(f"  Выходная директория: {output_dir}")
    print(f"  Количество частей: {n}×{n}")
    print(f"  Всего частей: {n * n}\n")


def get_args() -> Tuple[str, str]:
    """Получает аргументы командной строки."""
    if len(sys.argv) != 3:
        print("Использование: python puzzle.py <input_image> <output_dir>")
        print("Пример: python puzzle.py photo.jpg ./results")
        sys.exit(1)
    
    return sys.argv[1], sys.argv[2]


def main() -> None:
    """Основная функция программы."""
    try:
        # Получение аргументов
        input_path, output_dir = get_args()
        
        # Создание обработчика
        puzzle_maker = ImagePuzzle()
        
        # Загрузка изображения
        puzzle_maker.load_image(input_path)
        
        # Запрос количества частей
        n = get_n_from_user()
        
        # Показать сводку
        show_summary(input_path, output_dir, n)
        
        # Разделение на части
        tiles = puzzle_maker.split_image(n)
        
        # Перемешивание и сборка
        print("Перемешивание и сборка частей...")
        puzzle_maker.shuffle_and_build(tiles, n)
        
        # Сохранение результата
        puzzle_maker.save_result(output_dir)
        
        # Показ результатов
        puzzle_maker.show_comparison()
        
        print("Обработка завершена успешно!")
        
    except FileNotFoundError as e:
        print(f"Ошибка файла: {e}")
        sys.exit(1)
    except ValueError as e:
        print(f"Ошибка значения: {e}")
        sys.exit(1)
    except IOError as e:
        print(f"Ошибка ввода-вывода: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nПроцесс прерван пользователем.")
        sys.exit(0)
    except Exception as e:
        print(f"Неожиданная ошибка: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
