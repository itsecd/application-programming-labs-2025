import argparse
import os
import functions


def main():
    try:
        parser = argparse.ArgumentParser(
            description='Скачивание изображений по ключевому слову dog'
        )

        parser.add_argument("directory", type=str, help="путь к папке")
        parser.add_argument("annotation", type=str, help="путь к csv-файлу")

        args = parser.parse_args()

        directory = args.directory
        annotation = args.annotation

        functions.annotation_check(annotation)

        os.makedirs(directory, exist_ok=True)

        functions.clear_dir(directory)

        functions.download_images(directory, total_images=50)

        functions.make_grayscale(directory)

        functions.write_csv(annotation, directory)

        images = functions.AnnotationIterator(annotation)

        for img in images:
            print(img)

    except ValueError as e:
        print(e)
    except NotADirectoryError:
        print('ошибка пути к папке')
    except Exception as e:
        print('Ошибка:', e)


if __name__ == "__main__":
    main()
