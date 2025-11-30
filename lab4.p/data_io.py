from __future__ import annotations
from pathlib import Path
import pandas as pd


def load_annotation_csv(csv_path: str | Path) -> pd.DataFrame:
    """Загрузить CSV аннотацию."""
    csv_path = Path(csv_path)

    df = pd.read_csv(csv_path, sep=";")

    # Чистим названия колонок (убираем пробелы и BOM)
    df.columns = [c.strip().replace("\ufeff", "") for c in df.columns]

    return df


def save_dataframe(df: pd.DataFrame, output_path: str | Path, sep: str = ";") -> None:
    """Сохранить DataFrame в CSV."""
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False, sep=sep)