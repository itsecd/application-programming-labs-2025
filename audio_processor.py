"""Модуль для обработки аудиоданных и создания DataFrame."""
import pandas as pd
import numpy as np
from pathlib import Path
import librosa
import warnings
from typing import List, Dict, Optional
import config

warnings.filterwarnings('ignore')


class AudioProcessor:
    """Класс для обработки аудиоданных и создания DataFrame."""
    
    def __init__(self, annotation_file: Path, download_dir: Path) -> None:
        """Инициализация процессора с указанием файла аннотации и директории с аудиофайлами."""
        self.annotation_file = annotation_file
        self.download_dir = download_dir
        self.df: Optional[pd.DataFrame] = None
    
    def load_annotation_data(self) -> pd.DataFrame:
        """Загружает данные из CSV файла аннотации созданного во второй лабораторной работе."""
        try:
            if not self.annotation_file.exists():
                raise FileNotFoundError(f"Файл аннотации не найден")
            
            df = pd.read_csv(self.annotation_file)
            return df
            
        except Exception as e:
            print(f"Ошибка при загрузке аннотации: {e}")
            raise
    
    def analyze_audio_file(self, file_path: Path) -> Optional[Dict[str, float]]:
        """Анализирует аудиофайл и извлекает амплитудные характеристики включая диапазон (max-min)."""
        try:
            y, sr = librosa.load(file_path, sr=None, duration=30)
            
            amplitude = np.abs(y)
            max_amplitude = np.max(amplitude)
            min_amplitude = np.min(amplitude)
            mean_amplitude = np.mean(amplitude)
            amplitude_range = max_amplitude - min_amplitude
            
            duration = len(y) / sr
            rms_energy = np.sqrt(np.mean(y**2))
            
            return {
                'max_amplitude': float(max_amplitude),
                'min_amplitude': float(min_amplitude),
                'mean_amplitude': float(mean_amplitude),
                'amplitude_range': float(amplitude_range),
                'duration': float(duration),
                'rms_energy': float(rms_energy),
                'sample_rate': int(sr)
            }
            
        except Exception as e:
            print(f"Ошибка анализа файла {file_path.name}: {e}")
            return None
    
    def extract_instrument_from_filename(self, filename: str) -> str:
        """Извлекает название инструмента из имени файла по формату instrument_number_title.mp3."""
        parts = filename.lower().split('_')
        for part in parts:
            if part in config.INSTRUMENTS:
                return part
        return "unknown"
    
    def create_audio_dataframe(self) -> pd.DataFrame:
        """Создает DataFrame с информацией об аудиофайлах и их акустических характеристиках."""
        annotation_df = self.load_annotation_data()
        
        if annotation_df.empty:
            return pd.DataFrame()
        
        audio_data = []
        
        for index, row in annotation_df.iterrows():
            try:
                absolute_path = row.get('absolute_path', '')
                if not absolute_path:
                    continue
                
                file_path = Path(absolute_path)
                if not file_path.exists():
                    continue
                
                audio_features = self.analyze_audio_file(file_path)
                
                if audio_features:
                    filename = row.get('filename', file_path.name)
                    instrument = self.extract_instrument_from_filename(filename)
                    
                    audio_record = {
                        'filename': filename,
                        'instrument': instrument,
                        'absolute_path': str(file_path.absolute()),
                        'relative_path': row.get('relative_path', ''),
                        **audio_features
                    }
                    
                    audio_data.append(audio_record)
                        
            except Exception:
                continue
        
        if audio_data:
            return pd.DataFrame(audio_data)
        else:
            return pd.DataFrame()
    
    def add_amplitude_range_bins(self, df: pd.DataFrame) -> pd.DataFrame:
        """Добавляет колонку с диапазонами амплитуды для построения гистограммы распределения."""
        try:
            if 'amplitude_range' not in df.columns:
                return df
            
            min_range = df['amplitude_range'].min()
            max_range = df['amplitude_range'].max()
            ranges = np.linspace(min_range, max_range, config.BINS + 1)
            
            range_labels = []
            for i in range(len(ranges) - 1):
                range_labels.append(f"{ranges[i]:.3f}-{ranges[i+1]:.3f}")
            
            df['amplitude_range_bin'] = pd.cut(
                df['amplitude_range'], 
                bins=ranges, 
                labels=range_labels, 
                include_lowest=True
            )
            
            return df
            
        except Exception as e:
            print(f"Ошибка при добавлении колонки диапазонов: {e}")
            return df
    
    def sort_by_amplitude_range(self, df: pd.DataFrame, ascending: bool = True) -> pd.DataFrame:
        """Сортирует DataFrame по колонке с диапазоном амплитуды в указанном порядке."""
        return df.sort_values('amplitude_range', ascending=ascending)
    
    def filter_by_amplitude_range(self, df: pd.DataFrame, min_range: float, max_range: float) -> pd.DataFrame:
        """Фильтрует DataFrame оставляя только файлы с диапазоном амплитуды в указанных пределах."""
        return df[(df['amplitude_range'] >= min_range) & (df['amplitude_range'] <= max_range)]
    
    def process_audio_data(self) -> None:
        """Основной метод обработки данных: загрузка аннотации, анализ аудио и создание DataFrame."""
        try:
            annotation_df = self.load_annotation_data()
            
            if annotation_df.empty:
                print("Аннотация пуста или не загружена")
                return
            
            self.df = self.create_audio_dataframe()
            
            if self.df.empty:
                print("Не удалось создать DataFrame")
                return
            
            self.df = self.add_amplitude_range_bins(self.df)
            
        except Exception as e:
            print(f"Ошибка при обработке аудиоданных: {e}")
            raise