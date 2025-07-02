import sys
import random


from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton,
    QLineEdit, QHBoxLayout, QScrollArea, QFrame, QSizePolicy, QFileDialog, QMessageBox
)
from PyQt6.QtCore import Qt, QTimer, QThread, QObject, pyqtSignal
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import algorithm_consistent
import math
import re
from visualisation import Visualisation

class AlgorithmWorker(QObject):
    finished = pyqtSignal(object)
    error = pyqtSignal(str)

    def __init__(self, params):
        super().__init__()
        self.params = params

    def run(self):
        try:
            results = algorithm_consistent.run(**self.params)
            self.finished.emit(results)
        except Exception as e:
            self.error.emit(str(e))

class MainMenu(QWidget):
    def __init__(self, app):
        super().__init__()
        self.param_inputs = {}
        self.app = app
        self.initUI()
        
    def initUI(self):
        self.setStyleSheet("""
            background-color: #F2F2F2;
            color: black;
        """)

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.navbar = self.create_navbar("Main menu")
        layout.addWidget(self.navbar)

        content_layout = QVBoxLayout()
        content_layout.setContentsMargins(12, 5, 12, 12)
        content_layout.setSpacing(15)

        func_vis_frame = QFrame()
        func_vis_frame.setStyleSheet("""
            background-color: #ECE9E9;
            border-radius: 5px;
            padding: 5px;
        """)
        func_vis_frame.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
        )

        func_vis_layout = QVBoxLayout()

        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        self.canvas.setStyleSheet("background-color: white;")
        self.canvas.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
        )

        func_vis_layout.addWidget(self.canvas)
        func_vis_frame.setLayout(func_vis_layout)
        
        content_layout.addWidget(func_vis_frame)

        polynom_frame = QFrame()
        polynom_frame.setStyleSheet("""
            background-color: #ECE9E9;
            border-radius: 10px;
            padding: 3px 3px;
        """)
        polynom_frame.setFixedHeight(70)
        
        polynom_layout = QHBoxLayout()
        polynom_label = QLabel("f(x):")
        polynom_label.setStyleSheet("""
            font-family: Inter;
            font-weight: bold;
            color: black;
            font-size: 20px;
        """)
        
        self.polynom_input = QLineEdit()
        self.polynom_input.setEnabled(True)
        self.polynom_input.setStyleSheet("""
            background-color: white;
            border: 1px solid #ccc;
            height: 32px;
            border-radius: 3px;
            padding: 0 5px;
            font-size: 20px;
        """)
        self.polynom_input.setPlaceholderText("Enter function (e.g., sin(x)/x or x**2 + 3*x + 2")
        self.polynom_input.textChanged.connect(self.update_function_plot)

        generate_btn = QPushButton("Generate")
        generate_btn.setStyleSheet("""
            QPushButton {
                background-color: rgba(146, 231, 173, 1);
                color: rgba(0, 0, 0, 1);
                font-family: Inter;
                font-weight: bold;
                font-size: 20px;
                border-radius: 5px;
                border: none;
                min-width: 91px;
            }
            QPushButton:hover {
                background-color: #01b522;
            }
        """)
        generate_btn.setFixedHeight(50)
        generate_btn.clicked.connect(self.generate_random_polinomial)

        load_from_file_btn = QPushButton("Load from file")
        load_from_file_btn.setStyleSheet("""
            QPushButton {
                background-color: rgba(146, 231, 173, 1);
                color: rgba(0, 0, 0, 1);
                font-family: Inter;
                font-weight: bold;
                font-size: 20px;
                border-radius: 5px;
                border: none;
                min-width: 138px;
            }
            QPushButton:hover {
                background-color: #01b522;
            }
        """)
        load_from_file_btn.setFixedHeight(50)
        load_from_file_btn.clicked.connect(self.load_polynom_from_file)
        
        polynom_layout.addWidget(polynom_label)
        polynom_layout.addWidget(self.polynom_input)
        polynom_layout.addWidget(generate_btn)
        polynom_layout.addWidget(load_from_file_btn)

        polynom_layout.addStretch()
        polynom_frame.setLayout(polynom_layout)
        
        content_layout.addWidget(polynom_frame)

        right_column = QVBoxLayout()
        right_column.setSpacing(15)

        params_frame = QFrame()
        params_frame.setStyleSheet("""
            background-color: #ECE9E9;
            border-radius: 5px;
            margin-top: 2px;
            margin-right: 11.5px;
        """)
        params_frame.setMinimumSize(155, 213)
        params_frame.setMinimumHeight(350)
        
        params_layout = QVBoxLayout()
        params_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        params_layout.setSpacing(8)
        
        params_title = QLabel("PARAMETERS")
        params_title.setStyleSheet("""
            font-family: Inter;
            font-weight: bold;
            color: black;
            font-size: 28px;
            margin-bottom: 3px;
        """)
        params_layout.addWidget(params_title)
        
        params_list = [
            ("Iterations", "5"),
            ("Epochs", "15"),
            ("Population size", "15"),
            ("P_crossover", "0.7"),
            ("P_mutation", "0.1"),
            ("Tournament opponents", "2"),
            ("Alpha", "1")
        ]
        
        for name, default_val in params_list:
            param_layout = QHBoxLayout()
            
            label = QLabel(name)
            label.setStyleSheet("""
                font-family: Inter;
                color: black;
                font-size: 20px;
            """)
            label.setMinimumWidth(100)
            
            input_field = QLineEdit(default_val)
            self.param_inputs[name] = input_field
            input_field.setStyleSheet("""
                background-color: white;
                border: 1px solid #ccc;
                height: 28px;
                border-radius: 3px;
                padding: 0 5px;
                font-size: 20px;
            """)
            input_field.setFixedWidth(60 if name == "Alpha" else 71)
            
            param_layout.addWidget(label)
            param_layout.addWidget(input_field)
            params_layout.addLayout(param_layout)
        
        params_frame.setLayout(params_layout)
        right_column.addWidget(params_frame)

        borders_frame = QFrame()
        borders_frame.setStyleSheet("""
            background-color: #ECE9E9;
            border-radius: 5px;
            margin-bottom: 3px;
            margin-right: 11.5px;
        """)
        borders_frame.setFixedHeight(145)
        
        borders_layout = QVBoxLayout()
        
        borders_title = QLabel("Borders of usage")
        borders_title.setStyleSheet("""
            font-family: Inter;
            font-weight: bold;
            color: black;
            font-size: 22px;
        """)
        borders_layout.addWidget(borders_title, alignment=Qt.AlignmentFlag.AlignCenter)
        
        borders_inputs = QHBoxLayout()
        
        left_input = QVBoxLayout()
        left_input.setSpacing(4)
        left_label = QLabel("LEFT")
        left_label.setStyleSheet("""
            font-family: Inter;
            font-weight: bold;
            color: black;
            font-size: 20px;
        """)
        self.left_field = QLineEdit("-10")
        self.left_field.setStyleSheet("""
            background-color: white;
            border: 1px solid #ccc;
            height: 15px;
            border-radius: 3px;
            padding: 0 5px;
            font-size: 20px;
        """)
        self.left_field.setFixedWidth(60)
        self.left_field.setFixedHeight(50)
        self.left_field.textChanged.connect(self.update_function_plot)
        
        left_input.addWidget(left_label, alignment=Qt.AlignmentFlag.AlignCenter)
        left_input.addWidget(self.left_field, alignment=Qt.AlignmentFlag.AlignCenter)
        borders_inputs.addLayout(left_input)
        
        right_input = QVBoxLayout()
        right_input.setSpacing(4)
        right_label = QLabel("RIGHT")
        right_label.setStyleSheet("""
            font-family: Inter;
            color: black;
            font-weight: bold;
            font-size: 20px;
        """)
        self.right_field = QLineEdit("10")
        self.right_field.setStyleSheet("""
            background-color: white;
            border: 1px solid #ccc;
            height: 15px;
            border-radius: 3px;
            padding: 0 3px;
            font-size: 20px;
        """)
        self.right_field.setFixedWidth(60)
        self.right_field.setFixedHeight(50)
        self.right_field.textChanged.connect(self.update_function_plot)
        
        right_input.addWidget(right_label, alignment=Qt.AlignmentFlag.AlignCenter)
        right_input.addWidget(self.right_field, alignment=Qt.AlignmentFlag.AlignCenter)
        borders_inputs.addLayout(right_input)
        
        borders_layout.addLayout(borders_inputs)
        borders_frame.setLayout(borders_layout)
        right_column.addWidget(borders_frame)

        launch_btn = QPushButton("Launch Algorithm")
        launch_btn.setStyleSheet("""
            QPushButton {
                background-color: #33D13E;
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
                background-color: #01b522;
            }
        """)
        launch_btn.setFixedHeight(60)
        launch_btn.clicked.connect(self.launch_algorithm)
        right_column.addWidget(launch_btn, alignment=Qt.AlignmentFlag.AlignRight)

        main_content = QHBoxLayout()
        main_content.addLayout(content_layout, stretch=1)
        main_content.addLayout(right_column)
        
        layout.addLayout(main_content)
        self.setLayout(layout)

        self.update_function_plot()

    def launch_algorithm(self):
        try:
            self.create_loading_overlay()
            params = {
                'iterations': int(self.param_inputs["Iterations"].text()),
                'max_epochs': int(self.param_inputs["Epochs"].text()),
                'l': float(self.left_field.text()),
                'r': float(self.right_field.text()),
                'polinom': self.create_lambda(self.polynom_input.text().strip() or "sin(x)/x"),
                'population_size': int(self.param_inputs["Population size"].text()),
                'p_crossover': float(self.param_inputs["P_crossover"].text()),
                'p_mutation': float(self.param_inputs["P_mutation"].text()),
                'tournment_opponents': int(self.param_inputs["Tournament opponents"].text()),
                'alpha': float(self.param_inputs["Alpha"].text())
            }
            self.worker = AlgorithmWorker(params)
            self.thread = QThread()
            self.worker.moveToThread(self.thread)

            self.worker.finished.connect(self.on_algorithm_finished)
            self.worker.error.connect(self.on_algorithm_error)
            self.thread.started.connect(self.worker.run)
            self.worker.finished.connect(self.thread.quit)
            self.worker.error.connect(self.thread.quit)

            self.thread.start()

        except Exception as e:
            print(f"Error launching algorithm: {e}")
            if hasattr(self, 'loading_overlay'):
                self.loading_overlay.close()

    def on_algorithm_finished(self, results):
        self.app.current_results = results
        self.app.results.update_results(results)

        self.loading_overlay.close()

        iterations = int(self.param_inputs["Iterations"].text())
        max_epochs = int(self.param_inputs["Epochs"].text())
        self.app.visualisation = Visualisation(self.app, iterations, max_epochs)
        self.app.stacked_widget.removeWidget(self.app.stacked_widget.widget(2))
        self.app.stacked_widget.addWidget(self.app.visualisation)
        self.app.switch_to_visualisation()

    def on_algorithm_error(self, error_msg):
        print(f"Algorithm error: {error_msg}")
        if hasattr(self, 'loading_overlay'):
            self.loading_overlay.close()

        error_box = QMessageBox()
        error_box.setIcon(QMessageBox.Icon.Critical)
        error_box.setWindowTitle("Error")
        error_box.setText("An error occurred while running the algorithm:")
        error_box.setInformativeText(error_msg)
        error_box.exec()

    def create_loading_overlay(self):
        self.loading_overlay = QWidget(self)
        self.loading_overlay.setGeometry(0, 0, self.width(), self.height())
        self.loading_overlay.setStyleSheet("""
            background-color: rgba(2, 0, 79, 150);
        """)

        message_box = QFrame(self.loading_overlay)
        message_box.setStyleSheet("""
            background-color: #3156e8;
            border-radius: 10px;
            padding: 10px;
        """)
        message_box.setFixedSize(300, 150)

        layout = QVBoxLayout(message_box)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        loading_label = QLabel("Algorithm is running...")
        loading_label.setStyleSheet("""
            color: white;
            font-family: Arial;
            font-weight: bold;
            font-size: 18px;
        """)
        loading_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.spinner_label = QLabel("• • •")
        self.spinner_label.setStyleSheet("""
            color: white;
            font-family: Arial;
            font-size: 24px;
        """)
        self.spinner_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.spinner_counter = 0
        self.spinner_timer = QTimer()
        self.spinner_timer.timeout.connect(self.update_spinner)
        self.spinner_timer.start(500)  # Update every 500ms

        layout.addWidget(loading_label)
        layout.addWidget(self.spinner_label)
        message_box.setLayout(layout)

        message_box.move(
            (self.width() - message_box.width()) // 2,
            (self.height() - message_box.height()) // 2
        )

        self.loading_overlay.show()

    def update_spinner(self):
        self.spinner_counter = (self.spinner_counter + 1) % 4
        dots = "•" * self.spinner_counter
        self.spinner_label.setText(dots)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        if hasattr(self, 'loading_overlay'):
            self.loading_overlay.setGeometry(0, 0, self.width(), self.height())
            for child in self.loading_overlay.findChildren(QFrame):
                child.move(
                    (self.width() - child.width()) // 2,
                    (self.height() - child.height()) // 2
                )
    def update_function_plot(self):
        try:
            func_str = self.polynom_input.text().strip()
            if not func_str:
                func_str = "sin(x)/x"

            try:
                func = self.create_lambda(func_str)
            except:
                func = lambda x: math.sin(x) / x

            try:
                left = float(self.left_field.text())
            except:
                left = -10
            try:
                right = float(self.right_field.text())
            except:
                right = 10

            if right <= left:
                right = left + 1
            x, y = algorithm_consistent.getFunctionDots(1000, left, right, func)

            self.figure.clear()
            self.figure.set_facecolor('#ECE9E9')
            ax = self.figure.add_subplot(111)
            ax.plot(x, y, 'b-')
            ax.grid(True)
            ax.set_xlabel('x')
            ax.set_ylabel('f(x)')

            ax.set_title('Function Plot', fontdict={
                'fontsize': 22,
                'fontweight': 'normal'
            })

            self.canvas.draw()

        except Exception as e:
            print(f"Error plotting function: {e}")
    def generate_random_polinomial(self):
        result = ''
        for i in range(random.randint(2, 8)):
            result += f'({random.randint(1, 5)}/{random.randint(1, 5)}*x^{i})+'
        self.polynom_input.setText(result[:-1])


    def load_polynom_from_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Выберите файл с полиномом",
            "",
            "Текстовые файлы (*.txt);;Все файлы (*)"
        )
        if not file_path:
            return ""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                polynom_str = file.read().strip()
                self.polynom_input.setText(polynom_str)
        except Exception as e:
            print(f"Ошибка при чтении файла: {e}")
            return ""

    def create_lambda(self, func_str):
        func_str = func_str.replace('^', '**')

        math_funcs = ['sin', 'cos', 'tan', 'log', 'exp', 'sqrt', 'pi', 'e']
        for func in math_funcs:
            if func in func_str and f'math.{func}' not in func_str:
                func_str = func_str.replace(func, f'math.{func}')

        return eval(f'lambda x: {func_str}')
    
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
