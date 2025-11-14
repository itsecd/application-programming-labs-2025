import sys

from PyQt5 import QtWidgets

import main_window
from AudioIterator import AudioIterator


def show_info_messagebox(text: str) -> None:
    """Show message box with information"""
    msg = QtWidgets.QMessageBox()
    msg.setIcon(QtWidgets.QMessageBox.Information)
    msg.setText(text)
    msg.setWindowTitle("Infomration")
    msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
    msg.exec_()


def show_error_messagebox(text: str):
    """Show error message box with information about it"""
    msg = QtWidgets.QMessageBox()
    msg.setIcon(QtWidgets.QMessageBox.Critical)
    msg.setText(text)
    msg.setWindowTitle("Error")
    msg.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
    choice = msg.exec_()
    return choice


def get_audio() -> AudioIterator:
    """Get audio iterator for music direcotry"""
    folder_path = QtWidgets.QFileDialog.getExistingDirectory(
        caption="Select a folder where the audio files are located"
    )
    if folder_path is None:
        raise FileNotFoundError("Cannot find audiofiles")
    iterator = AudioIterator(folder_path)
    if len(iterator.paths) == 0:
        raise FileNotFoundError("Cannot find audiofiles")
    return iterator


def main() -> None:
    """Entry point. Setup Application"""
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = main_window.Ui_MainWindow()
    ui.setupUi(MainWindow)

    show_info_messagebox("Please, select the folder where the audio files are located")

    while True:
        try:
            iterator = get_audio()
            break
        except FileNotFoundError:
            choise = show_error_messagebox("Cannot find any audiofiles. Retry?")
            if choise == QtWidgets.QMessageBox.Yes:
                continue
            else:
                exit()

    ui.set_audio_iterator(iterator)

    MainWindow.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
