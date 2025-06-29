from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QGridLayout, QPushButton, QHBoxLayout
from PyQt6.QtGui import QDoubleValidator, QIntValidator


class SettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Настройки")
        self.setWindowModality(Qt.WindowModality.ApplicationModal)
        self.setFixedSize(600, 400)
        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setStyleSheet("""
            QDialog {
                background-color: #f8f9fa;
                border-radius: 20px;
                border: 2px solid #dee2e6;
            }
            QLabel {
                font-family: 'Inter';
                font-size: 24px;
                color: #495057;
            }
            QLineEdit {
                font-family: 'Inter';
                font-size: 24px;
                padding: 10px;
                border: 2px solid #bdc3c7;
                border-radius: 15px;
                background-color: white;
            }
            QPushButton {
                font-family: 'Inter';
                font-size: 24px;
                font-weight: bold;
                color: white;
                background-color: #0d6efd;
                border-radius: 15px;
                padding: 15px 30px;
                border: none;
            }
            QPushButton:hover {
                background-color: #0b5ed7;
            }
        """)
        title_label = QLabel("Настройки")
        title_label.setStyleSheet("""
            font-size: 32px;
            font-weight: bold;
            color: #212529;
            padding-bottom: 20px;
        """)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title_label)
        grid_layout = QGridLayout()
        grid_layout.setHorizontalSpacing(30)
        grid_layout.setVerticalSpacing(20)
        params = [
            ("Размер популяции:", "population_size", "15"),
            ("Вероятность скрещивания:", "crossover_prob", "0.7"),
            ("Вероятность мутации:", "mutation_prob", "0.1"),
            ("Количество эпох:", "epochs", "19")
        ]
        self.fields = {}
        for i, (label_text, field_name, default_value) in enumerate(params):
            label = QLabel(label_text)
            grid_layout.addWidget(label, i, 0, Qt.AlignmentFlag.AlignRight)
            line_edit = QLineEdit()
            line_edit.setObjectName(field_name)
            line_edit.setText(default_value)
            line_edit.setFixedHeight(50)
            if "вероятность" in label_text.lower():
                validator = QDoubleValidator(0.0, 1.0, 4)
                validator.setNotation(QDoubleValidator.Notation.StandardNotation)
            else:
                validator = QIntValidator(1, 1000000)
            line_edit.setValidator(validator)
            grid_layout.addWidget(line_edit, i, 1)
            self.fields[field_name] = line_edit
        main_layout.addLayout(grid_layout)
        button_layout = QHBoxLayout()
        button_layout.setSpacing(30)
        cancel_button = QPushButton("Отменить")
        cancel_button.setStyleSheet("background-color: #6c757d;")
        cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(cancel_button)
        save_button = QPushButton("Сохранить")
        save_button.clicked.connect(self.accept)
        button_layout.addWidget(save_button)
        main_layout.addSpacing(30)
        main_layout.addLayout(button_layout)
        self.setLayout(main_layout)

    def get_values(self):
        return {
            "population_size": int(self.fields["population_size"].text()),
            "crossover_prob": float(self.fields["crossover_prob"].text()),
            "mutation_prob": float(self.fields["mutation_prob"].text()),
            "epochs": int(self.fields["epochs"].text())
        }