from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QHBoxLayout,
                             QPushButton, QFrame, QTableWidget, QTableWidgetItem,
                             QHeaderView, QAbstractItemView, QSizePolicy)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont


class Results(QWidget):
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.initUI()

    def initUI(self):
        self.setStyleSheet("""
            background-color: #ECE9E9;
            color: black;
        """)

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.navbar = self.create_navbar("Results")
        layout.addWidget(self.navbar)

        content_layout = QVBoxLayout()
        content_layout.setContentsMargins(30, 20, 30, 30)
        content_layout.setSpacing(25)

        title_label = QLabel("Results")
        title_label.setFont(QFont("Inter", 32, QFont.Weight.Bold))
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        content_layout.addWidget(title_label)

        self.results_table = QTableWidget()
        self.results_table.setColumnCount(1)
        self.results_table.setHorizontalHeaderLabels(["Found maximum"])

        header = self.results_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        header.setFont(QFont("Inter", 20, QFont.Weight.Bold))
        header.setDefaultAlignment(Qt.AlignmentFlag.AlignCenter)

        self.results_table.verticalHeader().setVisible(False)
        self.results_table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.results_table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)

        self.results_table.setStyleSheet("""
            QTableWidget {
                background-color: white;
                border: 1px solid #cccccc;
                border-radius: 10px;
                gridline-color: #e0e0e0;
            }
            QHeaderView::section {
                background-color: #f0f0f0;
                padding: 15px;
                font-weight: bold;
                font-size: 20px;
                border: none;
            }
            QTableWidget::item {
                padding: 15px;
                font-size: 20px;
            }
        """)

        self.results_table.setMinimumHeight(400)
        content_layout.addWidget(self.results_table)

        layout.addLayout(content_layout)
        self.setLayout(layout)

    def update_results(self, results):
        self.results_table.setRowCount(len(results))

        for i in range(len(results)):
            self.results_table.setRowHeight(i, 60)

        for i, (x, y) in enumerate(results, 1):
            max_item = QTableWidgetItem(f"x = {x:.6f}, y = {y:.6f}")
            max_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            max_item.setFont(QFont("Inter", 18))
            self.results_table.setItem(i - 2, 1, max_item)

        self.results_table.resizeColumnsToContents()

    def create_navbar(self, active_tab):
        navbar = QWidget()
        navbar.setStyleSheet("background-color: #ECE9E9;")
        navbar.setFixedHeight(45)

        layout = QHBoxLayout()
        layout.setContentsMargins(12, 0, 12, 0)
        layout.setSpacing(0)

        tabs = [
            ("Main menu", lambda: self.app.switch_to_main_menu()),
            ("Visualisation", lambda: self.app.switch_to_visualisation()),
            ("Results", lambda: self.app.switch_to_results()),
            ("EXIT", lambda: self.app.closeEvent())
        ]

        for text, callback in tabs:
            btn = QPushButton(text)
            btn.setStyleSheet(f"""
                QPushButton {{
                    color: #000000;
                    font-family: 'Inter';
                    font-weight: bold;
                    font-size: 28px;
                    border: none;
                    padding: 10px 5px;
                    min-width: 80px;
                    background: {'#ED5151' if text == "EXIT" else '#33D13E' if text == active_tab else 'rgba(146, 231, 173, 1)'};
                }}
                QPushButton:hover {{
                    background: {'#c0392b' if text == "EXIT" else '#3395D1'}; 
                }}
            """)

            if text == "Main menu":
                separator = QFrame()
                separator.setFrameShape(QFrame.Shape.VLine)
                separator.setStyleSheet("background-color: black;")
                separator.setFixedWidth(2)
                layout.addWidget(separator)

            btn.clicked.connect(callback)
            layout.addWidget(btn)

            separator = QFrame()
            separator.setFrameShape(QFrame.Shape.VLine)
            separator.setStyleSheet("background-color: black;")
            separator.setFixedWidth(2)
            layout.addWidget(separator)

        navbar.setLayout(layout)
        return navbar
