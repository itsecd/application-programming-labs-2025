import cv2
import numpy as np
import random
import os

def create_puzzle(image_path, n):
    """Создает паззл из изображения"""
    print(f"Пытаемся загрузить: {image_path}")
    
    img = load_image_alternative(image_path)
    if img is None:
        raise ValueError(f"Не удалось загрузить изображение: {image_path}")
    
    print(f"Изображение успешно загружено, размер: {img.shape}")
    
    height, width = img.shape[0], img.shape[1]
    piece_height = height // n
    piece_width = width // n
    
    """Разрезает на кусочки"""
    pieces = []
    for i in range(n):
        for j in range(n):
            y_start = i * piece_height
            y_end = (i + 1) * piece_height
            x_start = j * piece_width
            x_end = (j + 1) * piece_width
            piece = img[y_start:y_end, x_start:x_end]
            pieces.append(piece)
    
    """Перемешивает и собирает обратно кусочки"""
    random.shuffle(pieces)
    
    puzzle = np.zeros_like(img)
    index = 0
    for i in range(n):
        for j in range(n):
            y_start = i * piece_height
            y_end = (i + 1) * piece_height
            x_start = j * piece_width
            x_end = (j + 1) * piece_width
            puzzle[y_start:y_end, x_start:x_end] = pieces[index]
            index += 1
    
    return img, puzzle

def load_image_alternative(image_path):
    """Альтернативный способ загрузки изображения(из-за проблем с кодировкой)"""
    try:
        """Пробует стандартный способ"""
        img = cv2.imread(image_path)
        if img is not None:
            return img
        
        """Пробует альтернативный способ"""
        with open(image_path, 'rb') as f:
            file_bytes = np.frombuffer(f.read(), np.uint8)
            img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
            return img
    except Exception as e:
        print(f"Ошибка загрузки: {e}")
        return None