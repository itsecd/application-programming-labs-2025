import csv
import os

def create_annotation_csv(images_path: str, csv_path: str) -> None:
    """
    create .csv file
    """


    images = []


    for f in os.listdir(images_path):
        name = f.lower()

        if name.endswith((".jpeg", ".jpg", ".png")):
            images.append(f)


    with open(csv_path, mode='w', newline='', encoding='utf-8-sig') as file:
        writer = csv.writer(file)

        writer.writerow(["absolute", "relative"])

        for filename in images:
            abs_path = os.path.abspath(os.path.join(images_path, filename))
            
            rel_path = os.path.relpath(abs_path, start=os.getcwd())
            writer.writerow([abs_path, rel_path])
