import pandas as pd

def create_dataframe_from_annotation(annotation_path: str) -> pd.DataFrame:
    """
    Формирование DataFrame
    :param annotation_path: Путь к аннотации
    :return: Сформированный DataFrame
    """
    df = pd.read_csv(annotation_path, header=None)
    return df
