from main_window import MainWindow
import sys
from PyQt5.QtWidgets import QApplication


def main(file_path: str) -> None:
    """
    Основная функция программы: создаёт Qt-приложение и отображает главное окно.

    Args:
        file_path (str): путь к файлу аннотации (annotation.csv),
                         который будет открыт при запуске.
    """
    app = QApplication(sys.argv)
    window = MainWindow(file_path)
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Lab 5 Audio Viewer")
    parser.add_argument("-f", "--file",type=str,help="Путь к файлу аннотации ",default="annotation.csv")
    args = parser.parse_args()

    try:
        main(args.file)
    except FileNotFoundError as e:
        print(f'Ошибка, не найден файл: "{e.filename}"')
    except PermissionError as e:
        print(f"Недостаточно прав для совершения операции: {e}")
    except Exception as e:
        print(f"Неожиданная ошибка: {e}")
