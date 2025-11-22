from download_images import parse_args, download_images, create_annotation, FileIterator
import cv2
import matplotlib.pyplot as plt

def print_shapes(path=str) -> None:
    img = cv2.imread(path)
    height, width, channels = img.shape
    print(f"Изображение \"{path}\" имеет размер: {height} выс., {width} шир., {channels} кан.")


def main() -> None:
    args = parse_args()

    try:
        download_images(args.output, args.keywords)
        create_annotation(args.output, args.annotation)

        files_iterator = FileIterator(args.output)
        for path in files_iterator:
            print_shapes(path)
            

           
    except Exception as e:
        print(f"Произошла ошибка: {e}")



if __name__ == "__main__":
    main()
       