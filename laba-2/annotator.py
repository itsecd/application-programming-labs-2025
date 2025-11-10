import csv
import os


def create_annotation(annotation_path: str, absolute_paths: list[str]) -> None:
    """
    Creates CSV annotation with absolute and relative paths.

    :param annotation_path: Filepath to save CSV annotation.
    :param absolute_paths: List of absolute paths to stored files.
    """
    try:
        with open(annotation_path, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)

            writer.writerow(["Absolute path", "Relative path"])

            for path in absolute_paths:
                relative_path = os.path.relpath(path)
                writer.writerow([path, relative_path])
        print("CSV annotation created.")
    except IOError as e:
        print(f"Error occurred while creating CSV: {e}")
