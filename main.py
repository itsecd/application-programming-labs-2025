import sys
from PyQt5 import QtWidgets
from player import MusicPlayer


def main():
    try:
        app = QtWidgets.QApplication([])
        window = MusicPlayer()
        window.setWindowTitle("FxntmPlayer")
        window.show()
        app.exec_()
    except Exception as e:
        print(f"Произошла ошибка: {e}")


if __name__ == "__main__":
    main()
