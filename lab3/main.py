import argparse
import matplotlib.pyplot as plt
import random
import cv2
import os
import numpy as np


parser = argparse.ArgumentParser(description='Обработка изображения')
parser.add_argument('--input_image', required=True, help='Изображение для обработки')
parser.add_argument('--output_dir', required=True, help='Папка для сохранения')
args = parser.parse_args()

img = cv2.imread(args.input_image)
if img is None:
    raise ValueError("Не удалось загрузить изображение")


height, width, channels = img.shape
print("Размер изображения =", width,"X", height)

height, width = img.shape[:2]

rows  = 4
cols = 4
# Вычисляем размеры каждой части
part_height = height // rows
part_width = width // cols

# Создаем список для хранения частей
pieces = []

# Разрезаем изображение на части
for i in range(rows):
    for j in range(cols):
        # Вырезаем часть
        piece = img[i * part_height:(i + 1) * part_height,
        j * part_width:(j + 1) * part_width]
        pieces.append(piece)

# Перемешиваем части
random.shuffle(pieces)

# Собираем изображение заново
puzzle = np.zeros((height, width, 3), dtype=np.uint8)

piece_index = 0
for i in range(rows):
    for j in range(cols):
        puzzle[i*part_height:(i+1)*part_height,
        j*part_width:(j+1)*part_width] = pieces[piece_index]
        piece_index += 1


if not os.path.exists(args.output_dir):
    os.makedirs(args.output_dir)

path = args.output_dir + 'beer.jpg'
cv2.imwrite(path ,  puzzle)

img1_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

# Отображение изображения
plt.imshow(img1_rgb)
plt.axis('off')  # Скрыть оси
plt.show()

img2_rgb = cv2.cvtColor(puzzle, cv2.COLOR_BGR2RGB)

# Отображение изображения
plt.imshow(img2_rgb)
plt.axis('off')  # Скрыть оси
plt.show()