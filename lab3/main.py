import cv2
import numpy
import os
from download_images import parse_args, download_images, create_annotation, FileIterator
import matplotlib.pyplot as plt 


def paint_frame(img: numpy.ndarray, height: int , width: int, thickness: int, color: tuple = (123,0,50)) -> None:
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

        frame_img_path = os.path.join(category_dir, f"frame_{os.path.basename(path)}")
        cv2.imwrite(frame_img_path, framed_img)
        print(f"Сохранено: {frame_img_path}")

def main() -> None:
    args = parse_args()

    try:
        download_images(args.output, args.keywords)
        create_annotation(args.output, args.annotation)
        arr_framed_imgs = {}

        files_iterator = FileIterator(args.output)
        for path in files_iterator:
            image = cv2.imread(path)      

            height, width, channels = image.shape
            image_shapes = f"{height} height x {width} width ({channels} channels)"

            paint_frame(image, height, width, int(width*0.02))
            arr_framed_imgs[path] = image

            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  # OpenCV использует BGR
            plt.figure(image_shapes)
            plt.imshow(image_rgb)

            plt.axis('off')  # убрать оси
            plt.show()
            
        save_new_images(arr_framed_imgs, args.result)
           
    except Exception as e:
        print(f"Произошла ошибка: {e}")


if __name__ == "__main__":
    main()
       