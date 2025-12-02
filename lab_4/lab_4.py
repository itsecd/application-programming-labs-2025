from __future__ import annotations
import argparse
from pathlib import Path
from typing import Tuple
import matplotlib.pyplot as plt
import pandas as pd
from PIL import Image


def get_image_dimensions(image_path: str | Path) -> Tuple[int, int]:
    """
    Возвращает размеры изображения (ширина, высота)

    Args:
        image_path: Путь к изображению

    Returns:
        (width, height) — кортеж из двух целых чисел
        (0, 0) — если файл не открылся
    """
    try:
        with Image.open(image_path) as img:
            return img.size
    except Exception as e:
        print(f"[Ошибка] Не удалось открыть {image_path}: {e}")
        return 0, 0


def create_dataframe_from_folder(folder_path: str | Path) -> pd.DataFrame:
    """
    Создаёт DataFrame со всеми изображениями из указанной папки

    Returns:
        pd.DataFrame с колонками:
            - Название файла
            - Абсолютный путь
            - Относительный путь
            - Ширина (px)
            - Высота (px)
            - Отношение сторон (ширина/высота)
    """
    folder = Path(folder_path).resolve()

    if not folder.is_dir():
        raise NotADirectoryError(f"Папка не найдена: {folder}")

    extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.webp', '.gif', '.heic', '.avif'}
    records = []

    for file_path in folder.iterdir():
        if file_path.suffix.lower() in extensions and file_path.is_file():
            width, height = get_image_dimensions(file_path)
            if width == 0 or height == 0:
                continue

            aspect_ratio = round(width / height, 4)

            records.append({
                'Название файла': file_path.name,
                'Абсолютный путь': str(file_path.absolute()),
                'Относительный путь': str(file_path.relative_to(Path.cwd())),
                'Ширина (px)': width,
                'Высота (px)': height,
                'Отношение сторон (ширина/высота)': aspect_ratio
            })

    df = pd.DataFrame(records)

    return df


def sort_by_aspect_ratio(df: pd.DataFrame, ascending: bool = False) -> pd.DataFrame:
    """Сортирует датафрейм по отношению сторон."""
    return df.sort_values(
        by='Отношение сторон (ширина/высота)',
        ascending=ascending
    ).reset_index(drop=True)


def filter_by_aspect_ratio(
    df: pd.DataFrame,
    min_ratio: float | None = None,
    max_ratio: float | None = None
) -> pd.DataFrame:
    """Фильтрует изображения по диапазону отношения сторон."""
    result = df.copy()
    col = 'Отношение сторон (ширина/высота)'

    if min_ratio is not None:
        result = result[result[col] >= min_ratio]
    if max_ratio is not None:
        result = result[result[col] <= max_ratio]

    return result.reset_index(drop=True)


def plot_aspect_ratios(df_sorted: pd.DataFrame, save_path: str = "aspect_ratio_plot.png") -> None:
    """Строит и сохраняет график отношения сторон."""
    ratios = df_sorted['Отношение сторон (ширина/высота)']
    x_labels = list(range(1, len(ratios) + 1))

    plt.figure(figsize=(14, 7))
    plt.plot(x_labels, ratios, 'o-', color='#2E86AB', markersize=6, linewidth=2, label='Отношение сторон')
    plt.fill_between(x_labels, ratios, alpha=0.1, color='#2E86AB')

    plt.title('Отношение сторон изображений (ширина ÷ высота)\nОтсортировано по убыванию', fontsize=16, pad=20)
    plt.xlabel('Номер изображения в отсортированном списке', fontsize=12)
    plt.ylabel('Отношение сторон (ширина / высота)', fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.4)
    plt.legend()
    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.show()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("folder", type=str, help="Путь к папке с изображениями")
    parser.add_argument(
        "--sort",
        choices=['asc', 'desc'],
        default='desc',
        help="Сортировка: asc — по возрастанию, desc — по убыванию "
    )
    parser.add_argument("--min", type=float, help="Минимальное отношение сторон ")
    parser.add_argument("--max", type=float, help="Максимальное отношение сторон ")

    args = parser.parse_args()

    df = create_dataframe_from_folder(args.folder)

    if df.empty:
        print("Изображения не найдены!")
        return

    print(f"Найдено изображений: {len(df)}")
    print(df[['Название файла', 'Ширина (px)', 'Высота (px)', 'Отношение сторон (ширина/высота)']].head(10))

    df_sorted = sort_by_aspect_ratio(df, ascending=(args.sort == 'asc'))

    df_final = filter_by_aspect_ratio(df_sorted, args.min, args.max)

    df_final.to_csv("images_analysis.csv", index=False, encoding='utf-8-sig')
    df_final.to_excel("images_analysis.xlsx", index=False)
    print(f"\nТаблица сохранена ({len(df_final)} строк):")
    print("images_analysis.csv")
    print("images_analysis.xlsx")

    plot_aspect_ratios(df_sorted)
    print("График сохранён: aspect_ratio_plot.png")

if __name__ == "__main__":
    main()