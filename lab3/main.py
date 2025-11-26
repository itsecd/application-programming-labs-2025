import cv2
import numpy
import os
from download_images import parse_args, download_images, create_annotation, FileIterator
import matplotlib.pyplot as plt 


def paint_frame(img: numpy.ndarray, height: int , width: int, thickness: int, color: tuple = (0, 0, 0)) -> None:
    """Рисование рамки на изображении"""
    x1 = thickness//2
    y1 = thickness//2
    x2 = width - thickness//2
    y2 = height - thickness//2

    thickness = min(thickness, (x2-x1)//2, (y2-y1)//2)

    cv2.rectangle(img, (x1,y1), (x2,y2), color, thickness)


def save_new_images(arr_imgs: dict, result_dir: str) -> None:
    """Сохранение изображений с рамками по ключевым словам в заданную директорию"""
    for path, framed_img in arr_imgs.items():
        category_dir = os.path.join(result_dir, os.path.basename(os.path.dirname(path)))
        os.makedirs(category_dir, exist_ok=True)

        framed_img_path = os.path.join(category_dir, f"frame_{os.path.basename(path)}")
        cv2.imwrite(framed_img_path, framed_img)
        print(f"Сохранено: {framed_img_path}")


def show_images(image: numpy.ndarray, image_shapes: str) -> None:
    """Выводит изображение вместе с его размерами"""
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    plt.figure(image_shapes)
    plt.imshow(image_rgb)

    plt.axis('off')
    plt.show()


def main() -> None:
    args = parse_args()

    try:
        download_images(args.output, args.keywords)
        create_annotation(args.output, args.annotation)
        arr_framed_imgs = {}

        files_iterator = FileIterator(args.annotation)
        for path in files_iterator:
            orig_image = cv2.imread(path)   
            framed_image = orig_image.copy() 

            height, width, channels = orig_image.shape
            image_shapes = f"{height} height x {width} width ({channels} channels)"

            paint_frame(framed_image, height, width, int(width*0.02), (123,0,50))
            arr_framed_imgs[path] = framed_image

            show_images(orig_image, image_shapes)
            show_images(framed_image, image_shapes)


        save_new_images(arr_framed_imgs, args.result)
           
    except Exception as e:
        print(f"Произошла ошибка: {e}")


if __name__ == "__main__":
    main()
       