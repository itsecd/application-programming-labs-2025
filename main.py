import pandas
import matplotlib as plt

def main(csv_path: str, output_frame: str, output_graph: str) -> None:
    """ 
    Основная логика программы 
    Args:
        csv_path (str): Файл для аннотаций на загруженные файлы
        output_frame (str): Путь для сохранения новых данных
        output_graph (str): Путь для сохранения графика
    """
    data = pandas.read_csv(csv_path)
    print(data)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()

    parser.add_argument("-c", "--csv", type=str, help="Путь к файлу аннотации", default="downloads/annotation.csv")
    parser.add_argument("-of", "--output_frame", type=str, help="Путь для сохранения новых данных", default="downloads/output.csv")
    parser.add_argument("-og", "--output_graph", type=str, help="Путь для сохранения графика", default="downloads/output.png")
    args = parser.parse_args()

    try:
        main(args.csv, args.output_frame, args.output_graph)
    except FileNotFoundError as e:
        print(f'Ошибка, не найден файл: "{e.filename}"')
    except PermissionError as e:
        print(f"Недостаточно прав для совершения операции: {e}")