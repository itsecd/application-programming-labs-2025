import argparse
import os
import sys
from Processing_images import process_all_images


def main():
    parser = argparse.ArgumentParser(description='Добавление рамки к изображениям')
    parser.add_argument('--input_folder', '-i', required=True, help='Папка с исходными изображениями')
    parser.add_argument('--output_folder', '-o', required=True, help='Папка для сохранения результатов')
    parser.add_argument('--frame_width', '-w', type=int, default=20, help='Ширина рамки в пикселях (по умолчанию: 20)')
    parser.add_argument('--frame_color', '-c', type=str, default='0,0,0', help='Цвет рамки в формате RGB (по умолчанию: 0,0,0 - черный)')
    
    args = parser.parse_args()
    
    if not os.path.exists(args.input_folder):
        print(f"Папка не существует: {args.input_folder}")
        sys.exit(1)
    
    try:
        color_values = [int(x.strip()) for x in args.frame_color.split(',')]
        if len(color_values) != 3:
            raise ValueError("Цвет должен содержать 3 значения: R,G,B")
        for value in color_values:
            if value < 0 or value > 255:
                raise ValueError("Значения цвета должны быть в диапазоне 0-255")
        frame_color = tuple(color_values)
    except ValueError as e:
        print(f"Ошибка в формате цвета: {e}")
        sys.exit(1)
    
    print(f"Исходные изображения: {args.input_folder}")
    print(f"Сохранение результатов: {args.output_folder}")
    print(f"Ширина рамки: {args.frame_width} пикселей")
    print(f"Цвет рамки: {frame_color}")
    print()
    
    process_all_images(args.input_folder, args.output_folder, args.frame_width, frame_color)

if __name__ == "__main__":
    main()
