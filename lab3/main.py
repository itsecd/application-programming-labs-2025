from download_images import parse_args, download_images, create_annotation, FileIterator
import cv2
import numpy

def paint_frame(img: numpy.ndarray, height: int , width: int, thickness: int, color: tuple = (123,0,50)) -> None:
    """Рисование рамки на изображении"""
    x1 = thickness//2
    y1 = thickness//2
    x2 = width - thickness//2
    y2 = height - thickness//2

    thickness = min(thickness, (x2-x1)//2, (y2-y1)//2)

    cv2.rectangle(img, (x1,y1), (x2,y2), color, thickness)


def main() -> None:
    args = parse_args()

    try:
        # download_images(args.output, args.keywords)
        create_annotation(args.output, args.annotation)
        image_array = []

        files_iterator = FileIterator(args.output)
        for path in files_iterator:
            image = cv2.imread(path)      

            height, width, channels = image.shape
            image_shapes = f"{height} height x {width} width ({channels} channels)"

            paint_frame(image, height, width, int(width*0.02))
            image_array.append(image)
            cv2.imshow(image_shapes, image)  # отображение
            cv2.waitKey(0)  

           
    except Exception as e:
        print(f"Произошла ошибка: {e}")


if __name__ == "__main__":
    main()
       