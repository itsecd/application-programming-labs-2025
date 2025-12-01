import cv2
import numpy as np
import matplotlib.pyplot as plt
import argparse
import csv
import os


def load_images(image_path1: str, image_path2: str) -> tuple:
    """
    Загрузка двух изображений
    """
    try:
        image1 = cv2.imread(image_path1)
        image2 = cv2.imread(image_path2)
        
        if image1 is None or image2 is None:
            print("Ошибка: не удалось загрузить изображения")
            return None, None
            
        return image1, image2
        
    except Exception as e:
        print(f"Ошибка при загрузке: {e}")
        return None, None


def get_dimensions(image: np.ndarray) -> tuple:
    """
    Получение размеров изображения
    """
    return image.shape[0], image.shape[1]


def combine_images(image1: np.ndarray, image2: np.ndarray) -> np.ndarray:
    """
    Объединение двух изображений
    """
    scale_factor = image1.shape[0] / image2.shape[0]
    new_width = int(image2.shape[1] * scale_factor)
    resized_image2 = cv2.resize(image2, (new_width, image1.shape[0]))
    
    combined = np.hstack((image1, resized_image2))
    return combined


def save_annotation(annotation_path: str, source1: str, source2: str, result_path: str, result_size: tuple) -> None:
    """
    Сохранение информации в файл аннотации
    """
    file_exists = os.path.exists(annotation_path)
    
    with open(annotation_path, 'a', newline='', encoding='utf-8') as annotation_file:
        writer = csv.writer(annotation_file)
        
        if not file_exists:
            writer.writerow(['Изображение 1', 'Изображение 2', 'Результат', 'Ширина', 'Высота'])
        
        height, width = result_size
        writer.writerow([source1, source2, result_path, width, height])
    
    print(f"Аннотация сохранена в: {annotation_path}")


def display_result(original: np.ndarray, result: np.ndarray) -> None:
    """
    Отображение оригинального и результирующего изображений
    """
    if len(original.shape) == 3 and original.shape[2] == 3:
        original_display = cv2.cvtColor(original, cv2.COLOR_BGR2RGB)
    else: 
        original_display = original

    if len(result.shape) == 3 and result.shape[2] == 3:
        result_display = cv2.cvtColor(result, cv2.COLOR_BGR2RGB)
    else: 
        result_display = result

    plt.subplot(2, 1, 1)
    plt.imshow(original_display)
    plt.axis('off')
    plt.title('Исходное изображение')

    plt.subplot(2, 1, 2)
    plt.imshow(result_display)
    plt.axis('off')
    plt.title('Объединенное изображение')

    plt.show()


def save_image(output_path: str, image: np.ndarray) -> None:
    """
    Сохранение изображения
    """
    if not output_path.endswith('.jpg'):
        output_path += '.jpg'
    
    cv2.imwrite(output_path, image)
    print(f"Изображение сохранено: {output_path}")


def main():
    """
    Основная функция
    """
    parser = argparse.ArgumentParser(description="Объединение изображений")
    parser.add_argument("--image_1", "-i1", default="fish_images/range_1/000001.jpg", 
                       type=str, help="Путь к первому изображению")
    parser.add_argument("--image_2", "-i2", default="fish_images/range_1/000002.jpg", 
                       type=str, help="Путь ко второму изображению")
    parser.add_argument("--result", "-r", default="result_image.jpg", 
                       type=str, help="Путь для сохранения результата")
    parser.add_argument("--annotation", "-a", default="annotation.csv", 
                       type=str, help="Файл аннотации (CSV)")
    
    args = parser.parse_args()

    # Загрузка изображений
    image1, image2 = load_images(args.image_1, args.image_2)
    
    if image1 is None or image2 is None:
        return
    
    # Получение размеров
    height1, width1 = get_dimensions(image1)
    print(f"Размер первого изображения: {width1}x{height1}")
    
    # Объединение изображений
    combined_image = combine_images(image1, image2)
    
    # Сохранение результата
    save_image(args.result, combined_image)
    
    # Сохранение аннотации
    result_height, result_width = get_dimensions(combined_image)
    save_annotation(args.annotation, args.image_1, args.image_2, 
                   args.result, (result_height, result_width))
    
    # Отображение результатов
    display_result(image1, combined_image)


if __name__ == "__main__":
    main()