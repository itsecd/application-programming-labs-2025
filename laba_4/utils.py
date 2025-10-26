import re


def get_correct_csv_path(csv_path: str) -> str:
    """
    Проверяет существует ли .csv в пути/названии или нет
    """
    match = re.search(r".csv$", csv_path)
    if match:
        return csv_path
    return csv_path + ".csv"
