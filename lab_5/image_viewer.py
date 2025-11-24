from __future__ import annotations

from typing import Optional

from PyQt6.QtWidgets import QLabel
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt


class ImageViewer(QLabel):
    """Виджет для отображения изображений с сохранением пропорций"""

    def __init__(self) -> None:
        super().__init__()
        self.original_pixmap: Optional[QPixmap] = None
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setStyleSheet(
            "QLabel { background-color: #f0f0f0; border: 1px solid #ccc; }"
        )
        self.setMinimumSize(400, 400)
        self.setText("Изображение не загружено")

    def load_image(self, path: str) -> None:
        """Загрузка и отображение изображения"""
        self.original_pixmap = QPixmap(path)
        if self.original_pixmap.isNull():
            raise ValueError(f"Не удалось загрузить изображение: {path}")
        self.update_display()

    def update_display(self) -> None:
        """Обновление отображения с сохранением пропорций"""
        if self.original_pixmap and not self.original_pixmap.isNull():
            scaled = self.original_pixmap.scaled(
                self.size(),
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation,
            )
            self.setPixmap(scaled)

    def resizeEvent(self, event) -> None:
        """Обработка изменения размера окна"""
        super().resizeEvent(event)
        self.update_display()

    def reset(self) -> None:
        """Очистка виджета"""
        self.original_pixmap = None
        self.setPixmap(QPixmap())
        self.setText("Изображение не загружено")