import argparse
import cv2
import matplotlib.pyplot as plt


def parsing() -> tuple[str, str, int]:
    parser = argparse.ArgumentParser()
    parser.add_argument("file_path", type=str, help="Enter file path")
    parser.add_argument("destination_path", type=str, help="Enter destination path")
    parser.add_argument("rotation_angle", type=int, help="Enter rotation angle")
    args = parser.parse_args()
    return args.file_path, args.destination_path, args.rotation_angle


def main():
    try:
        file_path, destination_path, rotation_angle = parsing()
        image = cv2.imread(file_path)
        shape = image.shape
        print(
            f"Ширина изображения в пикселях: {shape[1]} \n Высота изображения в пикселях:{shape[0]}"
        )
        rotation_matrix = cv2.getRotationMatrix2D(
            (shape[1] / 2, shape[0] / 2), rotation_angle, 1.0
        )
        modded_image = cv2.warpAffine(image, rotation_matrix, (shape[1], shape[0]))
        plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        plt.show()
        plt.imshow(cv2.cvtColor(modded_image, cv2.COLOR_BGR2RGB))
        plt.show()
        cv2.imwrite(destination_path, modded_image)
    except Exception as exp:
        print(exp)


if __name__ == "__main__":
    main()
