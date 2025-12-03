import argparse
import cv2
import numpy as np
import matplotlib.pyplot as plt
import os

def make_image(input_path, output_path, mode):
    """
    mode: black | white | transparent
    """
    img = cv2.imread(input_path, cv2.IMREAD_UNCHANGED)

    if img is None:
        raise FileNotFoundError(f"nothing file {input_path}")

    if img.shape[2] == 3:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)

    h, w = img.shape[:2]
    radius = min(h, w) // 2
    center = (w // 2, h // 2)

    mask = np.zeros((h, w), dtype=np.uint8)
    cv2.circle(mask, center, radius, 255, -1)

    result = img.copy()

    if mode == "transparent":
        result[:, :, 3] = mask

    elif mode in ["black", "white"]:
        bg_color = (0, 0, 0, 255) if mode == "black" else (255, 255, 255, 255)

        bg = np.zeros_like(result)
        bg[:] = bg_color

        mask_bool = mask.astype(bool)
        result = bg.copy()
        result[mask_bool] = img[mask_bool]

    else:
        raise ValueError("mode  black | white | transparent")

    cv2.imwrite(output_path, result)

    return img, result


def main():
    parser = argparse.ArgumentParser(description="modified image")
    parser.add_argument("input", help="path to image")
    parser.add_argument("output", help="output image")
    parser.add_argument("--mode", choices=["black", "white", "transparent"],
                        default="black", help="type")

    args = parser.parse_args()

    original, modified = make_image(args.input, args.output, args.mode)

    fig, axs = plt.subplots(1, 2, figsize=(12, 6))

    axs[0].imshow(cv2.cvtColor(original, cv2.COLOR_BGRA2RGBA))
    axs[0].axis("off")

    axs[1].imshow(cv2.cvtColor(modified, cv2.COLOR_BGRA2RGBA))
    axs[1].axis("off")

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()
