import os
import cv2
import matplotlib.pyplot as plt


def frame_adder(image_path: str, output_dir: str, file_counter: int) -> bool:
    """Накладывает рамку размером 20 пикселей на изображение"""
    try:
        image = cv2.imread(image_path)
        if image is None:
            print(f"Ошибка при загрузке: {image_path}")
            return False

        height, width = image.shape[:2]

        print(f"Обработка: {os.path.basename(image_path)}")
        print(f"   Размер: {width} x {height} пикселей")

        framed_image = image.copy()
        frame_width = 20
        black = (0, 0, 0)

        framed_image[0:height, 0:frame_width] = black
        framed_image[0:frame_width, 0:width] = black
        framed_image[0:height, (width-frame_width):width] = black
        framed_image[(height-frame_width):height, 0:width] = black

     
        filename = os.path.basename(image_path)
        name, extension = os.path.splitext(filename)
        new_filename = f"{file_counter:03d}{extension}"  
        output_path = os.path.join(output_dir, new_filename)
        
        success = cv2.imwrite(output_path, framed_image)

        if success:
            print(f"Сохранено: {new_filename}")
            show_difference(image, framed_image, filename)
            return True
        else:
            print(f"Ошибка сохранения: {new_filename}")
            return False

    except Exception as e:
        print(f"Ошибка при обработке {image_path}: {e}")
        return False


def show_difference(original: cv2.Mat, framed: cv2.Mat, filename: str) -> None:
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
        plt.title("С черной рамкой 20px", fontsize=12, pad=10)
        plt.axis('off')

        plt.tight_layout()
        plt.show()

    except Exception as e:
        print(f"Ошибка при отображении: {e}")