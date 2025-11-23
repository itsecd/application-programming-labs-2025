import numpy 
import cv2
import pandas as pd
import matplotlib.pyplot as plt 
from download_images import parse_args, download_images, create_annotation, FileIterator

def calc_range(img: numpy.ndarray) -> int:
    """Вычисление распределения диапазона яркости изображения по всем каналам""" 
    return numpy.ptp(img)


def add_col2df(df: pd.core.frame.DataFrame, col_name: str, img_iter: FileIterator, func) -> None:
    """Добавляет столбец к DataFrame'у"""
    df[col_name] = None; 
    for i, path in enumerate(img_iter):
        img = cv2.imread(path)
        df.loc[i, col_name] = func(img)


def sort_by_col(df: pd.core.frame.DataFrame, col_name: str,is_ascending: bool) -> None:
    """Сортирует DataFrame по указанному столбцу в заданном порядке"""
    df.sort_values(col_name, ascending=is_ascending, inplace=True)
    order = "возрастания" if is_ascending else "убывания"
    print(f"DataFrame отсортирован по столбцу {col_name} в порядке {order}.")


def filter_by_range(df: pd.core.frame.DataFrame, col_name: str, min_value: int, max_value: int) -> pd.core.frame.DataFrame:
    """Фильтрует DataFrame по указанному столбцу и диапазону"""
    return (df[(df[col_name] > min_value) & (df[col_name] < max_value)])


def create_range_gist(df: pd.DataFrame, res_path: str) -> None:
    """Создает график зависимости диапазона от номера в отсортированном DataFrame"""
    plt.hist(df['brightness_range'], bins=16)

    plt.title('Гистограмма распределения диапазонов')
    plt.xlabel('Значение диапазона')
    plt.ylabel('Количество файлов, подходящих под этот диапазон')

    plt.xticks(numpy.arange(0, 255, 16))
    plt.savefig(res_path, dpi=300, bbox_inches='tight')
    plt.show()


def main() -> None:
    args = parse_args()

    try:
        # download_images(args.output, args.keywords)
        create_annotation(args.output, args.annotation)

        df = pd.read_csv(args.annotation)

        new_col_name = "brightness_range"
        add_col2df(df, new_col_name, FileIterator(args.annotation), calc_range)

        sort_by_col(df, new_col_name, False)
        # filtered_df = filter_by_range(df, new_col_name, 10, 100)
        print(df)
        create_range_gist(df, args.histogram)

           
    except Exception as e:
        print(f"Произошла ошибка: {e}")


if __name__ == "__main__":
    main()
       