import argparse

import download_and_save
import show
import change_image

def parsing() -> tuple[str, str]:
    """
    передача аргументов через командную строку
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("filenamepathimage", type=str)
    parser.add_argument("filenamesave", type=str)
    args = parser.parse_args()
    return args.filenamepathimage, args.filenamesave


def main() -> None:
    try:
        filenamepath_image, filename_save = parsing()
        image = download_and_save.download_image(filenamepath_image)
        img_rgb, img_changed = change_image.change_image(image)
        show.show_image(img_rgb, img_changed)
        download_and_save.save_image(filename_save, img_changed)
    except Exception as exp:
        print(exp)


if __name__ == "__main__":
    main()

