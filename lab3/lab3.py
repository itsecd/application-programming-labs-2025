import argparse
import os
import cv2
import matplotlib.pyplot as plt # type: ignore

def parsing() -> argparse.Namespace:
    """Парсер аргументов"""
    parser = argparse.ArgumentParser()
    parser.add_argument('--path', type=str, required=True, help='path_to_files')
    parser.add_argument('--output', type=str, required=True, help='output_path')
    parser.add_argument('--width', type=int, required=True, help='output_width')
    parser.add_argument('--height', type=int, required=True, help='output_height')
    return parser.parse_args()

def show_images(original, cropped) -> None:
    """Вывод"""
    orig_rgb = cv2.cvtColor(original, cv2.COLOR_BGR2RGB)
    crop_rgb = cv2.cvtColor(cropped, cv2.COLOR_BGR2RGB)
    plt.imshow(orig_rgb)
    plt.title("Оригинальное")
    plt.show()
    plt.imshow(crop_rgb)
    plt.title("Обрезанное")
    plt.show()


def crop_images(path: str, output: str, new_width: int, new_height: int) -> None:
    """Обрезает изображения, сохраняет в файл и выводит"""
    if not os.path.exists(path):
        print("No such directory")
        return
    images = [i for i in os.listdir(path)]
    if not (os.path.exists(output)):
        os.mkdir(output)
    for i in images:
        input_path = os.path.join(path, i)
        output_path = os.path.join(output, i)
        img = cv2.imread(input_path)
        if img is None:
            print(f'ошибка при работе с {i}')
            continue
        height, width = img.shape[:2]
        print (f"размеры {i}: {width}x{height}")
        if (height < new_height) or (width < new_width):
            print (f"размеры {i} меньше, чем {new_width}x{new_height}")
            continue
        crop_img = img[0:new_height, 0:new_width]
        save = cv2.imwrite(output_path, crop_img)
        if not save:
            print(f"не удалось сохранить {i}")
            continue
        else:
            show_images(img, crop_img)

def main() -> None:
    args = parsing()
    crop_images(args.path, args.output, args.width, args.height)

if __name__ == '__main__':
    main()


        
