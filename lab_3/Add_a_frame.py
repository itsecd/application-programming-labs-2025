import os
import cv2
import matplotlib.pyplot as plt


def frame_adder(image_path: str, output_dir: str, file_counter: int, frame_width: int = 20, frame_color: tuple = (0, 0, 0)) -> bool:
    """Накладывает рамку на изображение"""
    try:
        image = cv2.imread(image_path)
        if image is None:
            return False

        height, width = image.shape[:2]

        framed_image = image.copy()

        framed_image[0:height, 0:frame_width] = frame_color
        framed_image[0:frame_width, 0:width] = frame_color
        framed_image[0:height, (width-frame_width):width] = frame_color
        framed_image[(height-frame_width):height, 0:width] = frame_color

        filename = os.path.basename(image_path)
        name, extension = os.path.splitext(filename)
        new_filename = f"{file_counter:03d}{extension}"  
        output_path = os.path.join(output_dir, new_filename)
        
        success = cv2.imwrite(output_path, framed_image)

        if success:
            show_difference(image, framed_image, filename, frame_width, frame_color)
            return True
        else:
            return False

    except Exception as e:
        return False


def show_difference(original: cv2.Mat, framed: cv2.Mat, filename: str, frame_width: int, frame_color: tuple) -> None:
    """Показывает сравнение исходного и обработанного изображения"""
    try:
        original_rgb = cv2.cvtColor(original, cv2.COLOR_BGR2RGB)
        framed_rgb = cv2.cvtColor(framed, cv2.COLOR_BGR2RGB)

        plt.figure(figsize=(12, 6))

        plt.subplot(1, 2, 1)
        plt.imshow(original_rgb)
        plt.title(f"Оригинал: {filename}", fontsize=12, pad=10)
        plt.axis('off')

        plt.subplot(1, 2, 2)
        plt.imshow(framed_rgb)
        plt.title(f"С рамкой {frame_width}px, цвет {frame_color}", fontsize=12, pad=10)
        plt.axis('off')

        plt.tight_layout()
        plt.show()

    except Exception as e:
        pass