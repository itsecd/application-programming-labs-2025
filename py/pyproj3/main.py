import argparse

import cv2

import imageworker



def main():
    try:

        parser = argparse.ArgumentParser(description="Преобразовывает изображение на пути path_in в размер size и сохраняет его по path_out")

        parser.add_argument("path_in", type=str, help="абсолютный путь до файла исходного изображения")
        parser.add_argument("path_out", type=str, help="путь для установки измененого изображения")
        parser.add_argument("size", type=str, help="размер нового изображения формата widthXheight")

        args = parser.parse_args()

        new_size = imageworker.size_format(args.size)

        image = cv2.imread(args.path_in)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        size = image.shape
        print(size)
        print(f"ширина = {size[1]}, высота = {size[0]}")


        resized_image = imageworker.change_size(image, new_size)

        imageworker.show_image(image, resized_image)

        cv2.imwrite(args.path_out, resized_image)

    except cv2.error as e:
        print(e)
    except ValueError as e:
        print(e)


if __name__ == "__main__":
    main()