from main_window import MainWindow
import sys
from PyQt5.QtWidgets import QApplication

def main(file_path: str) -> None:
    """ . . . """
    app = QApplication(sys.argv)
    window = MainWindow(file_path)
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", type=str, help="Путь к файлу аннотации", default="downloads/annotation.csv")
    args = parser.parse_args()

    try:
        main(args.file)
    except FileNotFoundError as e:
        print(f'Ошибка, не найден файл: "{e.filename}"')
    except PermissionError as e:
        print(f"Недостаточно прав для совершения операции: {e}")
