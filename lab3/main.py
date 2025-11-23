import argparse
import cv2
import functions


def main():
    try:
        parser = argparse.ArgumentParser(
            description="Поворачивает изображение на заданный угол."
        )

        parser.add_argument("path_in", type=str, help="Путь до исходного изображения")
        parser.add_argument("path_out", type=str, help="Путь сохранения результата")
        parser.add_argument("angle", type=float, help="Угол поворота в градусах")

        args = parser.parse_args()

        image = cv2.imread(args.path_in)
        if image is None:
            raise FileNotFoundError("Файл изображения не найден.")

        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        h, w = image.shape[:2]
        print(f"Размер изображения: {w}x{h} (ширина x высота)")

        rotated = functions.rotate_image(image, args.angle)

        functions.show_image(image, rotated)

        rotated_bgr = cv2.cvtColor(rotated, cv2.COLOR_RGB2BGR)
        cv2.imwrite(args.path_out, rotated_bgr)


    except Exception as e:
        print("Ошибка:", e)


if __name__ == "__main__":
    main()
