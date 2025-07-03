import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QHBoxLayout, QPushButton, QFrame, QTableWidget, QTableWidgetItem,
    QHeaderView, QAbstractItemView, QSizePolicy, QScrollArea
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont


class Results(QWidget):
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.max_points = []
        self.current_annotation = None
        self.initUI()
    
    def initUI(self):
        self.setStyleSheet("""
            background-color: #ECE9E9;
            color: black;
        """)
        
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        self.navbar = self.create_navbar("Results")
        main_layout.addWidget(self.navbar)

        content_widget = QWidget()
        content_layout = QHBoxLayout()
        content_layout.setContentsMargins(30, 20, 30, 30)
        content_layout.setSpacing(25)

        graph_area = QWidget()
        graph_layout = QVBoxLayout(graph_area)
        graph_title = QLabel("Graph of Maximum Values")
        graph_title.setFont(QFont("Inter", 24, QFont.Weight.Bold))
        graph_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        graph_layout.addWidget(graph_title)

        fig, ax = plt.subplots(figsize=(5, 4), dpi=100)
        self.canvas = FigureCanvas(fig)
        graph_layout.addWidget(self.canvas)

        self.canvas.mpl_connect('motion_notify_event', self.on_mouse_move)

        content_layout.addWidget(graph_area)

        table_scroll_area = QScrollArea()
        table_scroll_area.setWidgetResizable(True)
        table_container = QWidget()
        table_layout = QVBoxLayout(table_container)
        
        title_label = QLabel("Results")
        title_label.setFont(QFont("Inter", 32, QFont.Weight.Bold))
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        table_layout.addWidget(title_label)
        
        self.results_table = QTableWidget()
        self.results_table.setColumnCount(1)
        self.results_table.setHorizontalHeaderLabels(["Found maximum"])
        
        header = self.results_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
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
        self.results_table.cellClicked.connect(self.on_row_clicked)
        table_layout.addWidget(self.results_table)

        relaunch_btn = QPushButton("Re-launch Algorithm")
        relaunch_btn.setStyleSheet("""
            QPushButton {
                background-color: #FFD700;
                color: black;
                font-family: Inter;
                font-weight: bold;
                font-size: 24px;
                border-radius: 5px;
                border: none;
                min-width: 120px;
                margin-right: 11.5px;
                margin-bottom: 5px;
            }
            QPushButton:hover {
                background-color: #FFC000;
            }
        """)
        relaunch_btn.setFixedHeight(60)
        relaunch_btn.clicked.connect(self.relaunch_algorithm)
        table_layout.addWidget(relaunch_btn, alignment=Qt.AlignmentFlag.AlignRight)
        
        table_scroll_area.setWidget(table_container)
        content_layout.addWidget(table_scroll_area)

        main_layout.addLayout(content_layout)
        self.setLayout(main_layout)
    
    def relaunch_algorithm(self):
        self.app.main_menu.launch_algorithm()
    
    def on_mouse_move(self, event):
        if event.inaxes is not None:
            xdata, ydata = event.xdata, event.ydata
            points = [(x, y) for x, y in self.max_points]
            threshold = 0.5
            
            closest_point = None
            min_distance = float('inf')

            for point in points:
                dist = ((point[0] - xdata)**2 + (point[1] - ydata)**2)**0.5
                if dist < min_distance:
                    min_distance = dist
                    closest_point = point

            if min_distance <= threshold:
                self.annotate_point(closest_point)
            else:
                self.remove_annotation()

    def annotate_point(self, point):
        ax = self.canvas.figure.axes[0]
        if self.current_annotation:
            self.remove_annotation()

        annotation = ax.annotate(
            f"({point[0]:.2f}, {point[1]:.2f})",
            xy=point,
            xytext=(10, 10),
            textcoords="offset pixels",
            bbox=dict(boxstyle="round,pad=0.3", fc="w", ec="k", lw=1),
            arrowprops=dict(facecolor='black', shrink=0.05)
        )
        self.current_annotation = annotation
        self.canvas.draw_idle()

    def remove_annotation(self):
        if self.current_annotation:
            try:
                self.current_annotation.remove()
                self.current_annotation = None
            except Exception:
                self.current_annotation = None
            finally:
                self.canvas.draw_idle()

    def update_results(self, results):
        self.results_table.setRowCount(0)

        self.results_table.setRowCount(len(results))

        for i in range(len(results)):
            self.results_table.setRowHeight(i, 60)

        for i, (x, y) in enumerate(results):
            max_item = QTableWidgetItem(f"x = {x:.6f}, y = {y:.6f}")
            max_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            max_item.setFont(QFont("Inter", 18))
            self.results_table.setItem(i, 0, max_item)
        
        self.results_table.resizeColumnsToContents()
        
        self.max_points = results
        self.update_graph(results)
    
    def update_graph(self, data):
        if self.app.polinom is None or len(data) == 0:
            return
        
        self.canvas.figure.clear()
        ax = self.canvas.figure.add_subplot(111)

        x_min = self.app.left_border
        x_max = self.app.right_border
        x_range = np.linspace(x_min, x_max, 100)

        y_values = [self.app.polinom(x_range[i]) for i in range(len(x_range))]

        ax.plot(x_range, y_values, linewidth=2)

        ax.scatter([x for x, _ in data], [y for _, y in data], c='red', s=100, zorder=5, label="Maximal")

        ax.legend(loc="upper right")
        ax.grid(True)
        ax.set_xlabel("X-axis")
        ax.set_ylabel("Y-axis")
        
        self.canvas.draw()
    
    def on_row_clicked(self, row, col):
        if row >= 0 and row < len(self.max_points):
            point = self.max_points[row]
            self.annotate_point(point)

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