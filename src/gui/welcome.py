import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QPushButton, QLabel, QLineEdit, QSizePolicy, QGroupBox)
from PyQt6.QtCore import Qt, QEvent, QSize
from PyQt6.QtGui import QFont, QIcon


class GeneticAlgorithmGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Генетический алгоритм")
        self.setMinimumSize(900, 600)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(20, 15, 20, 20)
        main_layout.setSpacing(15)

        top_layout = QHBoxLayout()
        self.settings_button = QPushButton()
        self.settings_button.setIcon(QIcon("images/settings.png"))
        self.settings_button.setIconSize(QSize(60, 60))
        self.settings_button.setFixedSize(60, 60)
        self.settings_button.setStyleSheet(
            """
            QPushButton {
                background-color: transparent;
                border: none;
            }
            QPushButton:hover {
                background-color: #e0e0e0;
                border-radius: 10px;
            }
            """
        )
        top_layout.addWidget(self.settings_button)

        top_layout.addStretch()
        self.exit_button = QPushButton("Выйти")
        self.exit_button.setFont(QFont("Inter", 24))
        self.exit_button.setStyleSheet(
            """
            QPushButton {
                background-color: #ED5151;
                color: #000000;
                border-radius: 15px;
                padding: 15px 25px;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
            """
        )
        self.exit_button.clicked.connect(self.close)
        top_layout.addWidget(self.exit_button)
        main_layout.addLayout(top_layout)

        self.title_label = QLabel(
            "Поиск всех точек максимума полинома на интервале при помощи генетического алгоритма.")
        self.title_label.setFont(QFont("Inter", 24))
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title_label.setWordWrap(True)
        main_layout.addWidget(self.title_label)

        button_layout = QHBoxLayout()
        button_layout.setSpacing(30)

        self.load_button = QPushButton("Загрузить из файла")
        self.load_button.setFont(QFont("Inter", 24))
        self.load_button.setStyleSheet(
            """
            QPushButton {
                background-color: rgba(146, 231, 173, 0.75);
                color: rgba(0, 0, 0, 0.75);
                border-radius: 15px;
                padding: 15px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            """
        )

        self.generate_button = QPushButton("Сгенерировать случайно")
        self.generate_button.setFont(QFont("Inter", 24))
        self.generate_button.setStyleSheet(
            """
            QPushButton {
                background-color: rgba(146, 231, 173, 0.75);
                color: rgba(0, 0, 0, 0.75);
                border-radius: 15px;
                padding: 15px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            """
        )

        button_layout.addWidget(self.load_button)
        button_layout.addWidget(self.generate_button)

        button_container = QWidget()
        button_container.setLayout(button_layout)
        button_container.setSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Preferred)
        main_layout.addWidget(button_container, alignment=Qt.AlignmentFlag.AlignCenter)

        self.group = QGroupBox()
        self.group.setStyleSheet("QGroupBox { border: none; }")
        group_layout = QVBoxLayout(self.group)
        group_layout.setSpacing(30)

        polynomial_layout = QVBoxLayout()
        polynomial_layout.setSpacing(15)
        self.polynomial_label = QLabel("Введите полином (степень не больше 8)")
        self.polynomial_label.setFont(QFont("Inter", 24))
        polynomial_layout.addWidget(self.polynomial_label)

        self.polynomial_entry = QLineEdit()
        self.polynomial_entry.setFont(QFont("Inter", 24))
        self.polynomial_entry.setPlaceholderText("Введите полином...")
        self.polynomial_entry.setText("8*x^7 + 5*x^6 + 2*x^2")
        self.polynomial_entry.setStyleSheet(
            """
            QLineEdit {
                border: 2px solid #bdc3c7;
                border-radius: 15px;
                padding: 15px;
            }
            """
        )
        polynomial_layout.addWidget(self.polynomial_entry)
        group_layout.addLayout(polynomial_layout)

        interval_layout = QVBoxLayout()
        interval_layout.setSpacing(15)

        self.interval_label = QLabel("Введите границы интервала")
        self.interval_label.setFont(QFont("Inter", 24))
        interval_layout.addWidget(self.interval_label)

        interval_input_layout = QHBoxLayout()
        interval_input_layout.setSpacing(15)

        self.left_bracket = QLabel("[")
        self.left_bracket.setFont(QFont("Inter", 24))
        interval_input_layout.addWidget(self.left_bracket)

        self.min_entry = QLineEdit()
        self.min_entry.setFont(QFont("Inter", 24))
        self.min_entry.setText("-10")
        self.min_entry.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.min_entry.setStyleSheet(
            """
            QLineEdit {
                border: 2px solid #bdc3c7;
                border-radius: 15px;
                padding: 15px;
            }
            """
        )
        interval_input_layout.addWidget(self.min_entry)

        self.comma_label = QLabel(",")
        self.comma_label.setFont(QFont("Inter", 24))
        interval_input_layout.addWidget(self.comma_label)

        self.max_entry = QLineEdit()
        self.max_entry.setFont(QFont("Inter", 24))
        self.max_entry.setText("10")
        self.max_entry.setStyleSheet(
            """
            QLineEdit {
                border: 2px solid #bdc3c7;
                border-radius: 15px;
                padding: 15px;
            }
            """
        )

        interval_input_layout.addWidget(self.max_entry)
        self.right_bracket = QLabel("]")
        self.right_bracket.setFont(QFont("Inter", 24))
        interval_input_layout.addWidget(self.right_bracket)
        interval_layout.addLayout(interval_input_layout)
        group_layout.addLayout(interval_layout)

        self.run_button = QPushButton("Выполнить алгоритм")
        self.run_button.setFont(QFont("Inter", 24))
        self.run_button.setStyleSheet(
            """
            QPushButton {
                background-color: #92E7AD;
                color: 000000;
                border-radius: 15px;
                padding: 15px;
            }
            QPushButton:hover {
                background-color: #27ae60;
            }
            """
        )
        group_layout.addWidget(self.run_button, alignment=Qt.AlignmentFlag.AlignCenter)
        self.group.setSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Preferred)
        main_layout.addWidget(self.group, alignment=Qt.AlignmentFlag.AlignCenter)

        self.setup_connections()
        self.installEventFilter(self)
        self.showMaximized()

    def eventFilter(self, obj, event):
        if event.type() == QEvent.Type.Resize:
            self.group.setMaximumWidth(int(self.width() * 0.8))
            self.update_font_sizes()
        return super().eventFilter(obj, event)

    def update_font_sizes(self):
        base_size = min(40, int(min(self.width() / 40, self.height() / 28)))
        if self.height() < 700:
            new_font = QFont("Inter", 16)
        else:
            new_font = QFont("Inter", base_size)
        self.exit_button.setFont(new_font)
        self.title_label.setFont(new_font)
        self.load_button.setFont(new_font)
        self.generate_button.setFont(new_font)
        self.polynomial_label.setFont(new_font)
        self.polynomial_entry.setFont(new_font)
        self.interval_label.setFont(new_font)
        self.min_entry.setFont(new_font)
        self.max_entry.setFont(new_font)
        self.left_bracket.setFont(new_font)
        self.comma_label.setFont(new_font)
        self.right_bracket.setFont(new_font)
        self.run_button.setFont(new_font)

    def setup_connections(self):
        self.run_button.clicked.connect(self.run_algorithm)
        self.load_button.clicked.connect(self.load_from_file)
        self.generate_button.clicked.connect(self.generate_random)
        self.settings_button.clicked.connect(self.open_settings)

    def run_algorithm(self):
        print("Запуск алгоритма...")
        print(f"Полином: {self.polynomial_entry.text()}")
        print(f"Интервал: [{self.min_entry.text()}, {self.max_entry.text()}]")

    def load_from_file(self):
        print("Загрузка данных из файла...")

    def generate_random(self):
        print("Генерация случайных данных...")

    def open_settings(self):
        print("Открытие настроек...")


if __name__ == "__main__":
    app = QApplication([])
    window = GeneticAlgorithmGUI()
    window.show()
    sys.exit(app.exec())