from PyQt6.QtWidgets import QMainWindow, QStackedWidget, QApplication

from iteration import IterationViewer
from result import ResultPage
from welcome import WelcomePage


class MainApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Генетический алгоритм")
        self.setMinimumSize(900, 600)

        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        self.welcome_page = WelcomePage()
        self.iteration_viewer = IterationViewer()
        self.result_page = ResultPage()

        self.welcome_page.set_main_app(self)
        self.iteration_viewer.set_main_app(self)
        self.result_page.set_main_app(self)

        self.stacked_widget.addWidget(self.welcome_page)
        self.stacked_widget.addWidget(self.iteration_viewer)
        self.stacked_widget.addWidget(self.result_page)

        self.show_welcome_page()

    def show_welcome_page(self):
        self.stacked_widget.setCurrentWidget(self.welcome_page)

    def show_iteration_viewer(self):
        self.stacked_widget.setCurrentWidget(self.iteration_viewer)

    def show_result_page(self):
        self.result_page.set_iterations_data(self.iteration_viewer.iterations)
        self.stacked_widget.setCurrentWidget(self.result_page)
if __name__ == "__main__":
    app = QApplication([])
    main_app = MainApp()
    main_app.showMaximized()
    app.exec()