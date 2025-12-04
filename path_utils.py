import re


def get_correct_bild_path(bild_path: str) -> str:
    """
    Проверяет существует ли .jpg/jpeg/png в пути/названии или нет
    """
    match = re.search(r".(jpg|jpeg|png)$", bild_path)
    if match:
        return bild_path
    return bild_path + ".jpg"