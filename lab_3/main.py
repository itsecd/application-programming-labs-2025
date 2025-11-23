import argparse
import os
import sys
from Processing_images import process_all_images


def main():
    parser = argparse.ArgumentParser(description='Добавление черную рамку 20px к изображениям')
    parser.add_argument('--input_folder', '-i', required=True, help='Папка с исходными изображениями')
    parser.add_argument('--output_folder', '-o', required=True, help='Папка для сохранения результатов')
    
    args = parser.parse_args()
    
    if not os.path.exists(args.input_folder):
        print(f"Папка не существует: {args.input_folder}")
        sys.exit(1)
    
    process_all_images(args.input_folder, args.output_folder)


if __name__ == "__main__":
    main()
