import sys
import argparse
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont




def create_window():
    """
    Создаёт главное окно 
    """
    window = QMainWindow()
    window.setWindowTitle("Audio Dataset Viewer - Вариант 24")
    window.setGeometry(100, 100, 600, 300)
    
    # Создаём разметку
    layout = QVBoxLayout()
    layout.setSpacing(15)
    layout.setContentsMargins(20, 20, 20, 20)
    
    # Заголовок
    title = QLabel("Audio Player")
    title.setFont(QFont("Arial", 16, QFont.Bold))
    title.setAlignment(Qt.AlignCenter)
    layout.addWidget(title)
    
    # Тестовая кнопка
    test_button = QPushButton("Тестовая кнопка")
    layout.addWidget(test_button)
    
    layout.addStretch()
    
    # Устанавливаем разметку
    central_widget = QWidget()
    central_widget.setLayout(layout)
    window.setCentralWidget(central_widget)
    
    return window


def main():
    app = QApplication(sys.argv)
    window = create_window()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
