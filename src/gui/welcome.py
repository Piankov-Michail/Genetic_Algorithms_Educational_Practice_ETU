import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QPushButton, QLabel, QLineEdit, QSizePolicy,
                             QComboBox, QGridLayout, QDialog)
from PyQt6.QtCore import Qt, QEvent, QSize
from PyQt6.QtGui import QFont, QIcon

from settings import SettingsDialog


class WelcomePage(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Генетический алгоритм")
        self.setMinimumSize(900, 600)
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        self.settings = {
            "population_size": 15,
            "crossover_prob": 0.7,
            "mutation_prob": 0.1,
            "epochs": 15
        }

        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(20, 15, 20, 20)
        main_layout.setSpacing(15)

        top_layout = self.make_top_section()
        button_layout = self.make_buttons_section()
        polynomial_layout = self.make_polynomial_section()
        interval_layout = self.make_interval_section()
        self.make_run_button_section()

        main_layout.addLayout(top_layout)
        main_layout.addLayout(button_layout)
        main_layout.addLayout(polynomial_layout)
        main_layout.addLayout(interval_layout)
        main_layout.addWidget(self.run_button, alignment=Qt.AlignmentFlag.AlignCenter)

        self.setup_connections()
        self.installEventFilter(self)
        self.showMaximized()

    def make_top_section(self):
        top_layout = QVBoxLayout()
        buttons_layout = QHBoxLayout()
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
        buttons_layout.addWidget(self.settings_button)

        buttons_layout.addStretch()
        self.exit_button = QPushButton("Выйти")
        self.exit_button.setFont(QFont("Inter", 24))
        self.exit_button.setStyleSheet(
            """
            QPushButton {
                background-color: #ED5151;
                color: #000000;
                border-radius: 15px;
                padding: 8px;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
            """
        )
        buttons_layout.addWidget(self.exit_button)

        self.title_label = QLabel(
            "Поиск всех точек максимума полинома на интервале при помощи генетического алгоритма.")
        self.title_label.setFont(QFont("Inter", 24))
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title_label.setWordWrap(True)
        top_layout.addLayout(buttons_layout)
        top_layout.addWidget(self.title_label)
        return top_layout

    def make_buttons_section(self):
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
                padding: 8px;
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
                padding: 8px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            """
        )

        button_layout.addWidget(self.load_button)
        button_layout.addWidget(self.generate_button)
        return button_layout

    def make_polynomial_section(self):
        polynomial_layout = QVBoxLayout()
        polynomial_layout.setSpacing(30)

        degree_layout = QHBoxLayout()
        degree_layout.setSpacing(15)

        self.degree_label = QLabel("Выберите степень полинома:")
        self.degree_label.setFont(QFont("Inter", 24))
        degree_layout.addWidget(self.degree_label)

        self.degree_combo = QComboBox()
        self.degree_combo.setFont(QFont("Inter", 24))
        self.degree_combo.setMinimumHeight(60)
        self.degree_combo.setStyleSheet(
            """
            QComboBox {
                border: 2px solid #bdc3c7;
                border-radius: 15px;
                padding: 8px;
            }
            QComboBox::drop-down {
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 40px;
                border-left-width: 1px;
                border-left-color: #bdc3c7;
                border-left-style: solid;
                border-top-right-radius: 15px;
                border-bottom-right-radius: 15px;
            }
            """
        )
        for i in range(1, 9):
            self.degree_combo.addItem(str(i))
        self.degree_combo.setCurrentIndex(6)
        self.degree_combo.currentIndexChanged.connect(self.update_coefficient_fields)

        degree_layout.addWidget(self.degree_combo)
        degree_layout.addStretch()

        polynomial_layout.addLayout(degree_layout)
        self.coefficient_layout = QVBoxLayout()
        self.coefficient_layout.setSpacing(15)

        self.coefficient_label = QLabel("Введите коэффициенты полинома:")
        self.coefficient_label.setFont(QFont("Inter", 24))
        self.coefficient_layout.addWidget(self.coefficient_label)

        self.coeff_container = QWidget()
        self.coeff_container.setStyleSheet("background-color: transparent;")
        self.coeff_grid = QGridLayout(self.coeff_container)
        self.coeff_grid.setHorizontalSpacing(15)
        self.coeff_grid.setVerticalSpacing(15)
        self.coeff_grid.setContentsMargins(0, 0, 0, 0)

        self.coefficient_layout.addWidget(self.coeff_container)
        polynomial_layout.addLayout(self.coefficient_layout)

        self.coeff_widgets = []
        self.coeff_labels = []
        self.coeff_edits = []
        self.update_coefficient_fields()

        return polynomial_layout
    def make_interval_section(self):
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
        self.min_entry.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.min_entry.setStyleSheet(
            """
            QLineEdit {
                border: 2px solid #bdc3c7;
                border-radius: 15px;
                padding: 8px;
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
        self.max_entry.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.max_entry.setStyleSheet(
            """
            QLineEdit {
                border: 2px solid #bdc3c7;
                border-radius: 15px;
                padding: 8px;
            }
            """
        )

        interval_input_layout.addWidget(self.max_entry)

        self.right_bracket = QLabel("]")
        self.right_bracket.setFont(QFont("Inter", 24))
        interval_input_layout.addWidget(self.right_bracket)
        interval_layout.addLayout(interval_input_layout)

        return interval_layout
        
    def make_run_button_section(self):
        self.run_button = QPushButton("Выполнить алгоритм")
        self.run_button.setFont(QFont("Inter", 24))
        self.run_button.setStyleSheet(
            """
            QPushButton {
                background-color: #92E7AD;
                color: 000000;
                border-radius: 15px;
                padding: 8px;
            }
            QPushButton:hover {
                background-color: #27ae60;
            }
            """
        )

    def update_coefficient_fields(self):
        saved_values = []
        for edit in self.coeff_edits:
            saved_values.append(edit.text())
        for widget in self.coeff_widgets:
            widget.deleteLater()
        self.coeff_widgets.clear()
        self.coeff_labels.clear()
        self.coeff_edits.clear()
        degree = int(self.degree_combo.currentText())
        num_coeffs = degree + 1
        container_width = self.coeff_container.width()
        if container_width < 1:
            container_width = self.width() - 100
        widget_min_width = 80
        max_columns = max(1, min(9, container_width // widget_min_width))
        for i in range(num_coeffs):
            coeff_widget = QWidget()
            coeff_layout = QVBoxLayout(coeff_widget)
            coeff_layout.setSpacing(5)
            coeff_layout.setContentsMargins(0, 0, 0, 0)
            coeff_widget.setSizePolicy(
                QSizePolicy.Policy.MinimumExpanding,
                QSizePolicy.Policy.Fixed
            )
            coeff_widget.setMinimumWidth(40)
            exponent = degree - i
            label = QLabel(f"x<sup>{exponent}</sup>")
            label.setFont(QFont("Inter", 18))
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.coeff_labels.append(label)
            edit = QLineEdit()
            edit.setFont(QFont("Inter", 18))
            edit.setAlignment(Qt.AlignmentFlag.AlignCenter)
            edit.setStyleSheet(
                """
                QLineEdit {
                    border: 2px solid #bdc3c7;
                    border-radius: 10px;
                    padding: 5px;
                }
                """
            )
            edit.setMinimumWidth(60)
            if i < len(saved_values):
                edit.setText(saved_values[i])
            else:
                edit.setText("0")

            coeff_layout.addWidget(label)
            coeff_layout.addWidget(edit)
            self.coeff_widgets.append(coeff_widget)
            self.coeff_edits.append(edit)
        for i, widget in enumerate(self.coeff_widgets):
            row = i // max_columns
            col = i % max_columns
            self.coeff_grid.addWidget(widget, row, col)

        self.coeff_container.updateGeometry()

    def eventFilter(self, obj, event):
        if event.type() == QEvent.Type.Resize:
            self.update_font_sizes()
            self.redistribute_coefficients()
        return super().eventFilter(obj, event)

    def redistribute_coefficients(self):
        if not self.coeff_widgets:
            return
        container_width = self.coeff_container.width()
        if container_width < 1:
            return
        widget_min_width = 80
        max_columns = max(1, min(9, container_width // widget_min_width))
        while self.coeff_grid.count():
            item = self.coeff_grid.takeAt(0)
            widget = item.widget()
            if widget:
                self.coeff_grid.removeWidget(widget)
        for i, widget in enumerate(self.coeff_widgets):
            row = i // max_columns
            col = i % max_columns
            self.coeff_grid.addWidget(widget, row, col)

        self.coeff_container.updateGeometry()

    def update_font_sizes(self):
        base_size = min(28, int(min(self.width() / 45, self.height() / 33)))
        if self.height() < 900:
            new_font = QFont("Inter", 13)
            coeff_font = QFont("Inter", 10)
        else:
            new_font = QFont("Inter", base_size)
            coeff_font_size = max(10, min(18, int(self.width() / 30)))
            coeff_font = QFont("Inter", coeff_font_size)
        self.exit_button.setFont(new_font)
        self.title_label.setFont(new_font)
        self.load_button.setFont(new_font)
        self.generate_button.setFont(new_font)
        self.degree_label.setFont(new_font)
        self.degree_combo.setFont(new_font)
        self.coefficient_label.setFont(new_font)
        self.interval_label.setFont(new_font)
        self.min_entry.setFont(new_font)
        self.max_entry.setFont(new_font)
        self.left_bracket.setFont(new_font)
        self.comma_label.setFont(new_font)
        self.right_bracket.setFont(new_font)
        self.run_button.setFont(new_font)
        for label in self.coeff_labels:
            label.setFont(coeff_font)
        for edit in self.coeff_edits:
            edit.setFont(coeff_font)
    def check_polynomial(self):
        for i, edit in enumerate(self.coeff_edits):
            try:
                coeff = float(edit.text())
            except ValueError:
                coeff = 0.0
                print(f"Коэффициент {i+1} задан неверно")

    def setup_connections(self):
        self.exit_button.clicked.connect(self.close)
        self.degree_combo.currentIndexChanged.connect(self.update_coefficient_fields)
        self.run_button.clicked.connect(self.run_algorithm)
        self.load_button.clicked.connect(self.load_from_file)
        self.generate_button.clicked.connect(self.generate_random)
        self.settings_button.clicked.connect(self.open_settings)

    def run_algorithm(self):
        print("Запуск алгоритма...")
        print(f"Степень полинома: {self.degree_combo.currentText()}")
        coefficients = []
        for edit in self.coeff_edits:
            try:
                coeff = float(edit.text())
                coefficients.append(coeff)
            except ValueError:
                coefficients.append(0.0)

        print(f"Коэффициенты: {coefficients}")
        self.check_polynomial()
        print(f"Интервал: [{self.min_entry.text()}, {self.max_entry.text()}]")

    def load_from_file(self):
        print("Загрузка данных из файла...")

    def generate_random(self):
        print("Генерация случайных данных...")
        degree = int(self.degree_combo.currentText())
        for i in range(degree + 1):
            if i < len(self.coeff_edits):
                import random
                random_value = random.uniform(-100, 100)
                self.coeff_edits[i].setText(f"{random_value:.2f}")

    def open_settings(self):
        dialog = SettingsDialog(self)
        if dialog.exec() == QDialog.accepted:
            self.settings = dialog.get_values()


if __name__ == "__main__":
    app = QApplication([])
    window = WelcomePage()
    window.show()
    sys.exit(app.exec())