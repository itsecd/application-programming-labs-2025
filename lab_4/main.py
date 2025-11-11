import argparse

import cv2
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

def rang_calculate(path: str) -> int:
    """Вычисление диапазона яркости"""
    try:
        img = cv2.imread(path)
        if img is None:
            raise ValueError(f"Не удалось загрузить изображение: {path}")
        max_val = np.max(img)
        min_val = np.min(img)

        return max_val - min_val

    except Exception as e:
        print(f"Ошибка при вычислении диапазона яркости для {path}: {e}")
        return 0


def sort_by_brightness_range(df: pd.DataFrame) -> pd.DataFrame:
    """Сортировка таблички"""
    try:
        return df.sort_values(by="brightness range")
    except Exception as e:
        print(f"Ошибка при сортировке DataFrame: {e}")
        return df


def filter_by_brightness_range(df: pd.DataFrame, value: int) -> pd.DataFrame:
    """Фильтрация таблички по заданному значению"""
    try:
        return df[df["brightness range"] > value].reset_index(drop=True)
    except Exception as e:
        print(f"Ошибка при фильтрации DataFrame: {e}")
        return df


def parse_arguments():
    """Парсинг аргументов"""
    try:
        parser = argparse.ArgumentParser(description='Работа с pandas')
        parser.add_argument(
            '--input_csv',
            required=True,
            help='Исходный файл с путями'
        )
        return parser.parse_args()
    except Exception as e:
        print(f"Ошибка при парсинге аргументов: {e}")
        return None


def plot_brightness(df: pd.DataFrame) -> None:
    """Визуализация и сохранение графика"""
    try:
        plt.figure(figsize=(12, 6))
        plt.plot(range(len(df)), df.iloc[:, 2], marker='o', linewidth=2, markersize=4)
        plt.title('Диапазон яркости по изображениям')
        plt.xlabel('Номер изображения')
        plt.ylabel('Диапазон яркости')
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.savefig('brightness_plot.png', dpi=300, bbox_inches='tight')
        plt.show()
        print("График успешно сохранен в brightness_plot.png")

    except Exception as e:
        print(f"Ошибка при построении графика: {e}")


def main():
    """Основная функция"""
    try:
        # Парсинг аргументов
        args = parse_arguments()
        if args is None:
            print("Не удалось распарсить аргументы. Завершение работы.")
            return 0
        name = args.input_csv

        # Загрузка и обработка данных
        print(f"Загрузка данных из {name}...")
        df = pd.read_csv(name)
        df['brightness range'] = 0

        print("Вычисление диапазонов яркости...")
        for i in range(len(df)):
            df.iloc[i, 2] = rang_calculate(df.iloc[i, 1])

        # Сортировка и визуализация
        print("Сортировка данных...")
        df = sort_by_brightness_range(df)

        print("Построение графика...")
        plot_brightness(df)

        # Фильтрация
        print("Введите значение по которому фильтровать:")
        try:
            value = int(input())
        except ValueError:
            print("Ошибка: введите целое число!")
            return

        print(f"Фильтрация данных со значением > {value}...")
        df = filter_by_brightness_range(df, value)

        # Вывод и сохранение результатов
        print("\nРезультаты фильтрации:")
        print(df)

        print("Сохранение результатов в data.csv...")
        df.to_csv('data.csv', index=False)
        print("Программа успешно завершена!")

    except FileNotFoundError:
        print(f"Ошибка: файл {name} не найден!")
    except pd.errors.EmptyDataError:
        print("Ошибка: CSV файл пустой!")
    except pd.errors.ParserError:
        print("Ошибка: неверный формат CSV файла!")
    except KeyboardInterrupt:
        print("\nПрограмма прервана пользователем")
    except Exception as e:
        print(f"Неожиданная ошибка: {e}")


if __name__ == "__main__":
    main()