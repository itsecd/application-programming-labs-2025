import csv
import os
from typing import Iterator


class AudioFileIterator:
    """Iterator for audio files from a directory or CSV annotation file."""
    
    def __init__(self, source: str):
        """Initialize AudioFileIterator with source path.
        
        Args:
            source: Path to directory or CSV file with audio file paths
            
        Raises:
            ValueError: If source is not a valid directory or CSV file
        """
        self.paths = []

        if os.path.isdir(source):
            # Collect audio files from directory
            for root, _, files in os.walk(source):
                for file in files:
                    if file.lower().endswith(('.mp3', '.wav', '.ogg', '.m4a')):
                        full_path = os.path.join(root, file)
                        self.paths.append(full_path)
        elif os.path.isfile(source) and source.endswith(".csv"):
            # Collect paths from CSV file
            with open(source, encoding="utf-8") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if "absolute_path" in row:
                        self.paths.append(row["absolute_path"])
        else:
            raise ValueError(
                "Source must be a path to a CSV file or folder")

        self._index = 0

    def __iter__(self) -> Iterator[str]:
        """Return the iterator object."""
        return self

    def __next__(self) -> str:
        """Return the next audio file path.
        
        Returns:
            str: Path to audio file
            
        Raises:
            StopIteration: When no more files are available
        """
        if self._index >= len(self.paths):
            raise StopIteration
        
        path = self.paths[self._index]
        self._index += 1
        return path

    def __len__(self) -> int:
        """Return the number of audio files.
        
        Returns:
            int: Number of audio files available
        """
        return len(self.paths)