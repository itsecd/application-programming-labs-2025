import argparse
import cv2
import numpy
import os
import matplotlib.pyplot as plt


def download_image(filename_imagedata: str) -> numpy.ndarray:
    """
    Считывание изображения
    """
    img = cv2.imread(f"{filename_imagedata}\\000001.jpg")
    shape = img.shape
    print(shape)
    return img


def change_image(img: numpy.ndarray) -> tuple[numpy.ndarray, numpy.ndarray]:
    """
    Изменение изображения
    """
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img_changed = img_rgb[:, :, [2, 1, 0]]
    return img_rgb, img_changed


def show_image(img_rgb: numpy.ndarray, img_changed: numpy.ndarray) -> None:
    """
    Отображение изображения
    """
    plt.subplot(1, 2, 1)
    plt.imshow(img_rgb)
    plt.axis("off")
    plt.title("Image original")
    plt.subplot(1, 2, 2)
    plt.imshow(img_changed)
    plt.axis("off")
    plt.title("Image changed")
    plt.show()


def save_image(filename_save: str, img_changed: numpy.ndarray) -> None:
    """
    Сохранение изображения
    """
    if not os.path.exists(filename_save):
        os.mkdir(filename_save)
    output_path = os.path.join(filename_save, "output.jpg")
    cv2.imwrite(output_path, cv2.cvtColor(img_changed, cv2.COLOR_BGR2RGB))


def parsing() -> tuple[str, str]:
    """
    передача аргументов через командную строку
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("filenameimagedata", type=str)
    parser.add_argument("filenamesave", type=str)
    args = parser.parse_args()
    return args.filenameimagedata, args.filenamesave


def main() -> None:
    try:
        filename_imagedata, filename_save = parsing()
        image = download_image(filename_imagedata)
        img_rgb, img_changed = change_image(image)
        show_image(img_rgb, img_changed)
        save_image(filename_save, img_changed)
    except Exception as exp:
        print(exp)


if __name__ == "__main__":
    main()
