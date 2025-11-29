import pandas as pd
from image_processor import calculate_average_brightness

def create_dataframe_from_annotation(annotation_path: str) -> pd.DataFrame:
    """
    Формирование DataFrame
    :param annotation_path: Путь к аннотации
    :return: Сформированный DataFrame
    """
    df = pd.read_csv(annotation_path, header=None)
    return df



def name_columns(df: pd.DataFrame,
                 name_fist_column: str,
                 name_second_column: str) -> pd.DataFrame:
    """
    Именование колонок сформированного DataFrame
    :param df: сформированный DataFrame
    :param name_fist_column: Имя первой колонки
    :param name_second_column: Имя второй колонки
    :return: именованный DataFrame
    """
    first_row_values = df.iloc[0].astype(str).tolist()

    is_header_row = (name_fist_column in first_row_values) and (name_second_column in first_row_values)

    if is_header_row:

        df.columns = first_row_values

        df = df.iloc[1:].reset_index(drop=True)

        df.rename(columns={first_row_values[0]: name_fist_column,
                           first_row_values[1]: name_second_column}, inplace=True)

    else:
        rename_mapping = { df.columns[0]: name_fist_column,
                           df.columns[1]: name_second_column}
        
        df.rename(columns=rename_mapping, inplace=True)

    df = df[[name_fist_column, name_second_column]].copy()
    
    return df

def add_brightness_columns(df: pd.DataFrame,
                           name_fist_column: str) -> pd.DataFrame:
    """
    Добавление колонок со средними значениями яркости R, G, B
    :param df: сформированный с именами колонок DataFrame
    :param name_fist_column: Имя первой колонки
    :return: DataFrame с добавленными колонками со средними значениями яркости по каждому каналу
    """
    results = df[name_fist_column].apply(calculate_average_brightness)

    df["R"] = results.apply(lambda x: x[0])
    df["G"] = results.apply(lambda x: x[1])
    df["B"] = results.apply(lambda x: x[2])

    df.dropna(subset=["R", "G", "B"], inplace=True)

    return df
