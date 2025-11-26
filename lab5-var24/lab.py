from PyQt5.QtWidgets import QApplication, QMainWindow
import sys
from lab2_var24 import FileIterator

def get_songs_from_directory(dir_path: str) -> list:
    """
    Получает список всех MP3-файлов из папки с помощью FileIterator.
    
    
    """
    iterator = FileIterator(dir_path)
    songs = list(iterator)
    
    return songs

def create_main_window():
    """
    Создаёт основное окно приложения.
    """
    window = QMainWindow()
    window.setWindowTitle("Аудиоплеер - Датасет")
    window.setGeometry(100, 100, 800, 600)
    return window

def main():
    """
    Запуск приложения.
    """
    app = QApplication(sys.argv)
    window = create_main_window()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()