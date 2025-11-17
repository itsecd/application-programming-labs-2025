from __future__ import annotations

import argparse


def parse_args() -> argparse.Namespace:
    """Парсит аргументы командной строки."""
    parser = argparse.ArgumentParser(
        description="Полупрозрачное наложение одного изображения на другое.",
    )
    parser.add_argument(
        "img1",
        type=str,
        help="Путь к нижнему изображению",
    )
    parser.add_argument(
        "img2",
        type=str,
        help="Путь к накладываемому изображению",
    )
    parser.add_argument(
        "out",
        type=str,
        help="Путь для сохранения результата",
    )
    parser.add_argument(
        "--alpha",
        type=float,
        default=0.35,
        help="Прозрачность накладываемого (0..1), по умолчанию 0.35",
    )
    return parser.parse_args()