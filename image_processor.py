import random
from typing import Tuple

import cv2
import numpy as np


def create_puzzle(image: np.ndarray, n: int) -> Tuple[np.ndarray, np.ndarray]:
    """Создает паззл из изображения"""
    if n <= 0:
        raise ValueError("n должно быть положительным числом")
    
    height, width = image.shape[0], image.shape[1]
    
    if height < n or width < n:
        raise ValueError(f"Изображение слишком маленькое для разделения на {n}×{n} частей")
    
    piece_height = height // n
    piece_width = width // n
    
    height = piece_height * n
    width = piece_width * n
    image = image[:height, :width]
    
    pieces = []
    for i in range(n):
        for j in range(n):
            y_start = i * piece_height
            y_end = (i + 1) * piece_height
            x_start = j * piece_width
            x_end = (j + 1) * piece_width
            piece = image[y_start:y_end, x_start:x_end]
            pieces.append(piece)
    
    random.shuffle(pieces)
    
    puzzle = np.zeros_like(image)
    index = 0
    for i in range(n):
        for j in range(n):
            y_start = i * piece_height
            y_end = (i + 1) * piece_height
            x_start = j * piece_width
            x_end = (j + 1) * piece_width
            puzzle[y_start:y_end, x_start:x_end] = pieces[index]
            index += 1
    
    return image, puzzle