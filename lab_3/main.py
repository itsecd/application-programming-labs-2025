import cv2
import numpy as np
import matplotlib.pyplot as plt
import argparse
import os

def apply_gradient_lightening(image_path, output_path, direction='horizontal', intensity=1.0):
    """
    Применяет эффект градиентного осветления к изображению
    
    Параметры:
    - image_path: путь к исходному изображению
    - output_path: путь для сохранения результата
    - direction: 'horizontal' (слева → направо) или 'vertical' (сверху → вниз)
    - intensity: сила эффекта (0.0 — нет эффекта, 1.0 — максимальное осветление)
    """
    
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Файл не найден: {image_path}")

    
    img = cv2.imread(image_path)
    if img is None:
        raise ValueError(f"Не удалось загрузить изображение: {image_path}")

    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    height, width, channels = img_rgb.shape

    print(f"Загружено изображение: {width}×{height} пикселей, {channels} канала(ов)")

    result = img_rgb.astype(np.float32)

    if direction == 'horizontal':
        gradient = np.linspace(0, 1, width)
        gradient = np.tile(gradient, (height, 1))
    else:
        gradient = np.linspace(0, 1, height)
        gradient = np.tile(gradient, (width, 1)).T

    brightening = gradient[:, :, np.newaxis] * 100 * intensity
    result = result + brightening

    result = np.clip(result, 0, 255).astype(np.uint8)

    result_bgr = cv2.cvtColor(result, cv2.COLOR_RGB2BGR)
    cv2.imwrite(output_path, result_bgr)
    print(f"Результат сохранён: {output_path}")

    plt.figure(figsize=(15, 8))

    plt.subplot(1, 2, 1)
    plt.imshow(img_rgb)
    plt.title('Исходное изображение')
    plt.axis('off')

    plt.subplot(1, 2, 2)
    plt.imshow(result)
    plt.title(f'С градиентным осветлением\n({direction}, intensity={intensity})')
    plt.axis('off')

    plt.tight_layout()
    plt.show()

    return img_rgb, result


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Лабораторная работа №3: Градиентное осветление изображения")
    parser.add_argument("input", help="Путь к исходному изображению (jpg, png и т.д.)")
    parser.add_argument("output", help="Путь для сохранения результата")
    parser.add_argument("--direction", choices=['horizontal', 'vertical'], default='horizontal',
                        help="Направление градиента: horizontal (слева направо) или vertical (сверху вниз)")
    parser.add_argument("--intensity", type=float, default=1.0,
                        help="Сила осветления (0.0 — нет эффекта, 1.0 — стандарт, >1 — очень ярко)")

    args = parser.parse_args()

    try:
        original, processed = apply_gradient_lightening(
            image_path=args.input,
            output_path=args.output,
            direction=args.direction,
            intensity=args.intensity
        )
    except Exception as e:
        print(f"Ошибка: {e}")