import argparse

import pic_processing


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
        img = pic_processing.img_read(file_path)
        pic_processing.img_show(img)
        img_modded = pic_processing.img_rotation(img, rotation_angle)
        pic_processing.img_show(img_modded)
        pic_processing.img_writing(destination_path, img_modded)
    except Exception as exp:
        print(exp)


if __name__ == "__main__":
    main()
