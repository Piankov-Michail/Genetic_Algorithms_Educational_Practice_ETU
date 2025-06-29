from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QTableWidget, QAbstractItemView, QHeaderView, QHBoxLayout, \
    QPushButton, QTableWidgetItem, QSpacerItem, QSizePolicy


class ResultPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()

    def set_main_app(self, main_app):
        self.main_app = main_app

    def set_iterations_data(self, iterations):
        self.iterations = iterations
        self.update_table()

    def setup_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(30, 20, 30, 30)
        main_layout.setSpacing(25)

        title_label = QLabel("Результаты алгоритма")
        title_label.setFont(QFont("Inter", 32, QFont.Weight.Bold))
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title_label)

        table_container = QHBoxLayout()
        table_container.addItem(
            QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        )

        self.results_table = QTableWidget()
        self.results_table.setColumnCount(2)
        self.results_table.setHorizontalHeaderLabels(["Итерация", "Найденный максимум"])

        header = self.results_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        header.setFixedHeight(150)
        header.setDefaultAlignment(Qt.AlignmentFlag.AlignCenter)

        self.results_table.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Fixed)
        self.results_table.verticalHeader().setMinimumHeight(150)
        self.results_table.verticalHeader().setVisible(False)

        self.results_table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.results_table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.results_table.setStyleSheet("""
            QTableWidget {
                background-color: #ffffff;
                border: 1px solid #cccccc;
                border-radius: 10px;
                gridline-color: #e0e0e0;
            }
            QHeaderView::section {
                background-color: #f0f0f0;
                padding: 15px;
                font-weight: bold;
                font-size: 32px;
                border: none;
            }
            QTableWidget::item {
                padding: 15px;
                font-size: 32px;
            }
        """)

        self.results_table.setMinimumWidth(800)
        self.results_table.setMinimumHeight(500)

        table_container.addWidget(self.results_table, 1)

        table_container.addItem(
            QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        )

        main_layout.addLayout(table_container, 1)

        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(30)
        buttons_layout.setContentsMargins(0, 20, 0, 0)

        self.back_button = QPushButton("Вернуться к итерациям")
        self.back_button.setFont(QFont("Inter", 28))
        self.back_button.setMinimumSize(250, 80)
        self.back_button.setStyleSheet(
            "QPushButton {"
            "   background-color: #2196F3;"
            "   color: white;"
            "   border-radius: 10px;"
            "}"
            "QPushButton:hover {"
            "   background-color: #0b7dda;"
            "}"
        )
        self.back_button.clicked.connect(self.goto_iterations)
        buttons_layout.addWidget(self.back_button)

        self.restart_button = QPushButton("Запустить снова")
        self.restart_button.setFont(QFont("Inter", 28))
        self.restart_button.setMinimumSize(250, 80)
        self.restart_button.setStyleSheet(
            "QPushButton {"
            "   background-color: #4CAF50;"
            "   color: white;"
            "   border-radius: 10px;"
            "}"
            "QPushButton:hover {"
            "   background-color: #45a049;"
            "}"
        )
        self.restart_button.clicked.connect(self.restart_algorithm)
        buttons_layout.addWidget(self.restart_button)

        self.new_params_button = QPushButton("Новые параметры")
        self.new_params_button.setFont(QFont("Inter", 28))
        self.new_params_button.setMinimumSize(250, 80)
        self.new_params_button.setStyleSheet(
            "QPushButton {"
            "   background-color: #f1f1f1;"
            "   border-radius: 10px;"
            "   border: 1px solid #cccccc;"
            "}"
            "QPushButton:hover {"
            "   background-color: #e9e9e9;"
            "}"
        )
        self.new_params_button.clicked.connect(self.new_parameters)
        buttons_layout.addWidget(self.new_params_button)

        main_layout.addLayout(buttons_layout)

        self.setLayout(main_layout)
        self.setStyleSheet("background-color: white; border-radius: 15px; padding: 15px;")

    def update_table(self):
        if not hasattr(self, 'iterations'):
            return

        self.results_table.setRowCount(len(self.iterations))

        for i in range(len(self.iterations)):
            self.results_table.setRowHeight(i, 80)

        for i, iteration in enumerate(self.iterations):
            iteration_item = QTableWidgetItem(iteration["title"])
            iteration_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            iteration_item.setFont(QFont("Inter", 28))
            self.results_table.setItem(i, 0, iteration_item)

            max_value = iteration["max"]
            max_item = QTableWidgetItem(f"{max_value:.6f}")
            max_item.setFont(QFont("Inter", 28))
            max_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.results_table.setItem(i, 1, max_item)

        self.results_table.resizeColumnsToContents()

        if self.iterations:
            self.results_table.selectRow(len(self.iterations) - 1)

    def goto_iterations(self):
        self.main_app.show_iteration_viewer()

    def restart_algorithm(self):
        self.main_app.iteration_viewer.current_iteration = 0
        self.main_app.iteration_viewer.update_view()
        self.main_app.show_iteration_viewer()

    def new_parameters(self):
        self.main_app.show_welcome_page()