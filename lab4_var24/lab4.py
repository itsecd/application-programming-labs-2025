import pandas as pd 

def load_csv(path_csv):
    """
    Читаем csv файл
    """
    return pd.read_csv(path_csv)



