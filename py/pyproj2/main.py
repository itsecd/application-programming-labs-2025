import argparse
import os

import  helpers


def main():
    try:
        parser = argparse.ArgumentParser(description='Скачивает изображения по ключевому слову rabbit')
        parser.add_argument("directory", type=str, help="Путь до папки")
        parser.add_argument("annotation", type=str, help="Путь до файла анотации")
        parser.add_argument("ranges", nargs='+', type=helpers.parse_size_range, help="Диапазоны размеров изображений в формате: minWxminH-maxWxmaxH. Например: 100x100-300x300 500x500-800x800")

        args = parser.parse_args()

        annotation = args.annotation.split('/')[-1]
        directory = args.directory.split('/')[-1]

        helpers.annotation_check(annotation)

        os.makedirs(directory, exist_ok=True)

        helpers.clear_dir(directory)

        helpers.download_images(args.ranges, directory)

        helpers.write_csv(annotation, directory)

        images_paths = helpers.AnnotationIterator(annotation)

        for image_path in images_paths:
            print(image_path)


    except IndexError:
        print('Ошибка в вводе ranges')
    except ValueError as e:
        print(e)
    except NotADirectoryError:
        print('Ошибка в вводе directory')

if __name__ == "__main__":
    main()