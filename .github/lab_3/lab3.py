import cv2
import numpy
import matplotlib.pyplot as plt
import argparse

def puller(img1: str, img2: str) -> tuple:
    """
    Преобразование файла в картинку
    """
    res1 = cv2.imread(img1)
    res2 = cv2.imread(img2)
    if res1 is None or res2 is None:
        raise FileNotFoundError
    return res1, res2


def size(img: numpy.ndarray)->tuple:
    """
    Получение размеров картинки 
    """
    return img.shape[0], img.shape[1]


def union_img(img1: numpy.ndarray, img2: numpy.ndarray) -> numpy.ndarray:
    """
    объединение двух картинок
    """
    changer = img1.shape[0]/img2.shape[0]
    img2 = cv2.resize(img2, (int(img2.shape[1]*changer), img1.shape[0]))
    comb = numpy.hstack((img1, img2))
    return comb


def show_img(img: numpy.ndarray) -> None:
    """
    Демонстрация отдельной картинки
    (не пригодилось)
    """
    plt.imshow(img)
    plt.axis('off')
    plt.show()


def res_show(img: numpy.ndarray, change_img: numpy.ndarray) -> None:
    """
    Демонстрация исходной картинки и результата
    """
    if len(img.shape) == 3 and img.shape[2] == 3:
        img_show = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    else: 
        img_show = img
    
    if len(change_img.shape) == 3 and change_img.shape[2] == 3:
        change_img_show = cv2.cvtColor(change_img, cv2.COLOR_BGR2RGB)
    else: 
        change_img_show = change_img

    plt.subplot(2, 1, 1)
    plt.imshow(img_show)
    plt.axis('off')
    plt.title('Было')

    plt.subplot(2, 1, 2)
    plt.imshow(change_img_show)
    plt.axis('off')
    plt.title('Стало')

    plt.show()


def save_to_file(filename: str, img: numpy.ndarray) -> None:
    """
    сохранение картинки в формате jpg файла
    """
    if not filename.endswith('.png'):
        filename += '.png'
    cv2.imwrite(filename, img)


def main():

    parser = argparse.ArgumentParser(description="Извлечение данных из файла на основе шаблонов.")
    parser.add_argument("--image_1", "-i1", default="image/000001.jpg", type=str, help="Путь к исходной картинке.")
    parser.add_argument("--image_2", "-i2", default="image/000002.jpg", type=str, help="Путь к каринке с которой будет происходить совмещение.")
    parser.add_argument("--res_file", "-r", default="result_lab3", type=str, help="Путь к файлу для записи результата.")
    args = parser.parse_args()

    img1, img2 = puller(args.image_1, args.image_2)
    cv2.imshow('img', img2)
    print(size(img1))


    comb = union_img(img1, img2)
    save_to_file(args.res_file, comb)
    res_show(img1, comb)


if __name__ == "__main__":
    main()