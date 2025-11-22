from download_images import parse_args, download_images, create_annotation, FileIterator
import cv2
import numpy

def shape_str(img=numpy.ndarray) -> str:
    height, width, channels = img.shape
    return f"{height} height x {width} width ({channels} channels)"

def paint_frame(img=numpy.ndarray) -> None:
    cv2.rectangle(img, (50, 50), (200, 150), (0, 255, 0), 3)



def main() -> None:
    args = parse_args()

    try:
        # download_images(args.output, args.keywords)
        create_annotation(args.output, args.annotation)
        img_array = []

        files_iterator = FileIterator(args.output)

        for path in files_iterator:
            img = cv2.imread(path)
            img_shapes = shape_str(img)
            paint_frame(img)
            img_array.append(img)
            cv2.imshow(img_shapes, img)  # отображение
            cv2.waitKey(0)  

           
    except Exception as e:
        print(f"Произошла ошибка: {e}")



if __name__ == "__main__":
    main()
       