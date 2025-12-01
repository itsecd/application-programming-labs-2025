import argparse
import cv2
import numpy as np
import matplotlib.pyplot as plt

def main():
    parser = argparse.ArgumentParser(description="Поменять местами цветовые каналы изображения (например: BGR → RGB или RGB → GBR и т.д.)")
    parser.add_argument("--input", "-i", required=True, help="Путь к входному изображению")
    parser.add_argument("--output", "-o", required=True, help="Путь для сохранения результата")
    parser.add_argument("--order", "-r", type=str, default="2,1,0", 
                        help="Порядок каналов (по умолчанию '2,1,0' → BGR → RGB). "
                             "Индексация: 0=R, 1=G, 2=B для RGB-изображения. "
                             "Например: '1,0,2' — поменять R и G (GRB), '2,0,1' — B,R,G и т.д.")
    args = parser.parse_args()

    """ Загрузка изображения """
    img_bgr = cv2.imread(args.input)
    if img_bgr is None:
        raise FileNotFoundError(f"Не удалось загрузить изображение: {args.input}")

    print(f"Размер изображения: {img_bgr.shape} (H, W, C)")
    h, w, c = img_bgr.shape
    if c != 3:
        raise ValueError("Поддерживаются только 3-канальные (цветные) изображения.")

    """ Переводим из BGR (OpenCV) в RGB для удобства интерпретации """
    img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)

    """ Парсинг порядка каналов """
    try:
        order = list(map(int, args.order.split(',')))
        if len(order) != 3 or not all(0 <= x <= 2 for x in order):
            raise ValueError
    except:
        raise ValueError("Некорректный формат --order. Должно быть три индекса через запятую (например: '2,1,0').")

    """ Перестановка каналов """
    img_swapped = img_rgb[:, :, order]

    """ Отображение исходного и преобразованного изображений """
    plt.figure(figsize=(12, 5))

    plt.subplot(1, 2, 1)
    plt.imshow(img_rgb)
    plt.title("Исходное изображение (RGB)")
    plt.axis("off")

    plt.subplot(1, 2, 2)
    plt.imshow(img_swapped)
    plt.title(f"Результат: порядок каналов [{','.join(map(str, order))}]")
    plt.axis("off")

    plt.tight_layout()
    plt.show()

    """ Сохранение: OpenCV ожидает BGR, поэтому конвертируем обратно """
    img_swapped_bgr = cv2.cvtColor(img_swapped, cv2.COLOR_RGB2BGR)
    cv2.imwrite(args.output, img_swapped_bgr)
    print(f"Результат сохранён: {args.output}")

if __name__ == "__main__":
    main()