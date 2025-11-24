import sys
from PyQt6 import QtWidgets
from main_window import MainWindow
from load_images import create_annotation



def main():
    try:
        create_annotation("images", "annotation_paths.csv")
        app = QtWidgets.QApplication(sys.argv)
        main_window = MainWindow()

        main_window.show()
        sys.exit(app.exec())
    except Exception as e:
        print(f"Произошла ошибка: {e}")


if __name__ == "__main__":
    main()
