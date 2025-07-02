import os
import sys
import shutil
from PyQt6.QtWidgets import QApplication, QStackedWidget, QMainWindow
from PyQt6.QtGui import QPalette, QColor
from PyQt6.QtCore import Qt
from main_menu import MainMenu
from results import Results
from visualisation import Visualisation


def clean_frames_folder():
    folder = 'frames'
    if not os.path.exists(folder):
        return

    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print(f"Ошибка удаления {file_path}: {e}")

    try:
        shutil.rmtree(folder)
    except Exception as e:
        print(f"Ошибка удаления {folder}: {e}")


class MainWindow(QMainWindow):
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.current_results = []
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        palette = QPalette()
        palette.setColor(QPalette.ColorRole.Window, QColor(2, 0, 79))
        palette.setColor(QPalette.ColorRole.WindowText, Qt.GlobalColor.white)
        palette.setColor(QPalette.ColorRole.Base, QColor(35, 86, 232))
        palette.setColor(QPalette.ColorRole.AlternateBase, QColor(2, 0, 79))
        palette.setColor(QPalette.ColorRole.ToolTipBase, Qt.GlobalColor.white)
        palette.setColor(QPalette.ColorRole.ToolTipText, Qt.GlobalColor.white)
        palette.setColor(QPalette.ColorRole.Text, Qt.GlobalColor.white)
        palette.setColor(QPalette.ColorRole.Button, QColor(35, 86, 232))
        palette.setColor(QPalette.ColorRole.ButtonText, Qt.GlobalColor.white)
        palette.setColor(QPalette.ColorRole.BrightText, Qt.GlobalColor.red)
        palette.setColor(QPalette.ColorRole.Highlight, QColor(42, 130, 218))
        palette.setColor(QPalette.ColorRole.HighlightedText, Qt.GlobalColor.black)
        self.app.setPalette(palette)

        self.app.setStyleSheet("""
            QWidget {
                font-family: "Inter";
                background-color: #F2F2F2;
            }
            QPushButton {
                min-width: 80px;
                padding: 5px;
            }
        """)

        self.main_menu = MainMenu(self)
        self.results = Results(self)
        self.visualisation = Visualisation(self, 5, 15)

        self.stacked_widget.addWidget(self.main_menu)
        self.stacked_widget.addWidget(self.results)
        self.stacked_widget.addWidget(self.visualisation)

        self.stacked_widget.setCurrentWidget(self.main_menu)
        self.setMinimumSize(900, 600)
        self.setWindowTitle("Genetic Algorithm")

    def closeEvent(self):
        clean_frames_folder()
        quit()

    def switch_to_main_menu(self):
        self.stacked_widget.setCurrentWidget(self.main_menu)

    def switch_to_results(self):
        self.stacked_widget.setCurrentWidget(self.results)

    def switch_to_visualisation(self):
        self.stacked_widget.setCurrentWidget(self.visualisation)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.aboutToQuit.connect(clean_frames_folder)

    main_window = MainWindow(app)
    main_window.show()
    sys.exit(app.exec())
