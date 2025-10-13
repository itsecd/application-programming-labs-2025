import csv




CSV_HEADER = ["genre", "abs_path", "real_path", "url", ]

def csv_init(csv_path) -> None:
    """
    Создаёт CSV-файл с заголовком
    """

    with open(csv_path, 'w', encoding= "utf-8", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(CSV_HEADER)


def append_to_csv(csv_path, genre, abs_path, real_path, url) -> None:
    """
    добавляет строки  в CSV-файл
    """

    with open(csv_path, 'a', encoding= "utf-8", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([genre, abs_path, real_path, url])

