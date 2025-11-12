"""Конфигурационные параметры проекта."""
from pathlib import Path

# Пути к данным
DATA_DIR = Path(".")  # Текущая директория
DOWNLOAD_DIR = DATA_DIR / "audio"  # Папка с аудиофайлами
ANNOTATION_FILE = DATA_DIR / "annotation.csv"  # Файл аннотации

# Файлы вывода
OUTPUT_DF_FILE = DATA_DIR / "audio_analysis.csv"  
OUTPUT_PLOT_FILE = DATA_DIR / "amplitude_range_histogram.png"

# Настройки гистограммы
BINS = 8

# Инструменты для анализа
INSTRUMENTS = ["trumpet", "ukulele", "harp"]