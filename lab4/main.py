import cv2
import pandas as pd
import matplotlib.pyplot as plt 
from download_images import parse_args, download_images, create_annotation, FileIterator

def main() -> None:
    args = parse_args()
    # pd.set_option('display.max_colwidth', None)

    try:
        download_images(args.output, args.keywords)
        create_annotation(args.output, args.annotation)
        image_iterator = FileIterator(args.annotation)
        df = pd.read_csv(args.annotation)

        df["brightness_range"] = None; 
        for i, path in enumerate(image_iterator):
            image = cv2.imread(path)
        
            df.loc[i, "brightness_range"] = image.max() - image.min()
        print(df.head())
           
    except Exception as e:
        print(f"Произошла ошибка: {e}")


if __name__ == "__main__":
    main()
       