from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout,
    QFrame, QSizePolicy
)
from PyQt6.QtGui import QFont, QMovie
from PyQt6.QtCore import Qt, QSize


class IterationViewer(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        self.iterations = [
            {"title": "1 итерация", "max": -27.16004, "gif": "animation_0.gif"},
            {"title": "2 итерация", "max": 21.23754, "gif": "animation_1.gif"},
            {"title": "3 итерация", "max": -2.36407, "gif": "animation_2.gif"}
        ]
        self.current_iteration = 0
        self.update_view()

    def set_main_app(self, main_app):
        self.main_app = main_app

    def set_algorithm_data(self, degree, coefficients, interval, settings):
        self.degree = degree
        self.coefficients = coefficients
        self.interval = interval
        self.settings = settings

    def setup_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(30, 20, 30, 30)

        header_layout = QHBoxLayout()

        self.title_label = QLabel()
        self.title_label.setFont(QFont("Inter", 28))
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        header_layout.addWidget(self.title_label)

        header_layout.addStretch(1)

        self.result_button = QPushButton("Перейти к результату")
        self.result_button.setFont(QFont("Inter", 28))
        self.result_button.setStyleSheet(
            "QPushButton {"
            "   background-color: #4CAF50;"
            "   color: white;"
            "   border-radius: 10px;"
            "}"
            "QPushButton:hover {"
            "   background-color: #45a049;"
            "}"
            "QPushButton:disabled {"
            "   background-color: #cccccc;"
            "}"
        )
        self.result_button.clicked.connect(self.goto_result)
        header_layout.addWidget(self.result_button, alignment=Qt.AlignmentFlag.AlignRight)

        main_layout.addLayout(header_layout)

        self.graph_label = QLabel()
        self.graph_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.graph_label.setMinimumSize(1200, 700)
        self.graph_label.setStyleSheet("background-color: #f0f0f0; border-radius: 10px;")
        main_layout.addWidget(self.graph_label)

        max_container = QWidget()
        max_layout = QHBoxLayout(max_container)
        max_layout.setContentsMargins(0, 0, 0, 0)

        self.max_label = QLabel()
        self.max_label.setFont(QFont("Inter", 28))
        self.max_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.max_label.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        self.max_label.setMinimumHeight(80)
        max_layout.addWidget(self.max_label)

        main_layout.addWidget(max_container, alignment=Qt.AlignmentFlag.AlignCenter)
        nav_layout = QHBoxLayout()
        nav_layout.setSpacing(20)
        nav_layout.setContentsMargins(0, 10, 0, 0)
        nav_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.prev_button = QPushButton("Предыдущая итерация")
        self.prev_button.setFont(QFont("Inter", 28))
        self.prev_button.setStyleSheet(
            "QPushButton {"
            "   background-color: #f1f1f1;"
            "   border-radius: 8px;"
            "   border: 1px solid #cccccc;"
            "}"
            "QPushButton:hover {"
            "   background-color: #e9e9e9;"
            "}"
        )
        self.prev_button.clicked.connect(self.prev_iteration)
        nav_layout.addWidget(self.prev_button)

        self.next_button = QPushButton("Следующая итерация")
        self.next_button.setFont(QFont("Inter", 28))
        self.next_button.setStyleSheet(
            "QPushButton {"
            "   background-color: #2196F3;"
            "   color: white;"
            "   border-radius: 10px;"
            "}"
            "QPushButton:hover {"
            "   background-color: #0b7dda;"
            "}"
        )
        self.next_button.clicked.connect(self.next_iteration)
        nav_layout.addWidget(self.next_button)

        main_layout.addLayout(nav_layout)

        self.setLayout(main_layout)
        self.setStyleSheet("background-color: white; border-radius: 15px; padding: 15px;")

    def update_view(self):
        data = self.iterations[self.current_iteration]
        self.title_label.setText(data["title"])
        self.max_label.setText(f"Найден максимум при <i>x</i> = {data['max']}")
        movie = QMovie(data['gif'])
        self.graph_label.setMovie(movie)
        movie.setScaledSize(QSize(800, 500))
        movie.start()
        self.prev_button.setVisible(self.current_iteration > 0)
        self.next_button.setVisible(self.current_iteration < len(self.iterations) - 1)

    def next_iteration(self):
        if self.current_iteration < len(self.iterations) - 1:
            self.current_iteration += 1
            self.update_view()

    def prev_iteration(self):
        if self.current_iteration > 0:
            self.current_iteration -= 1
            self.update_view()

    def goto_result(self):
        self.main_app.show_result_page()
