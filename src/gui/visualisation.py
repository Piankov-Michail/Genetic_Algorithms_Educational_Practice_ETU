from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QPushButton,
                             QHBoxLayout, QFrame, QSlider, QLineEdit, QSizePolicy)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QIcon, QIntValidator, QPixmap


class Visualisation(QWidget):
    def __init__(self, app, iterations=5, epochs=15):
        super().__init__()
        self.app = app
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_visualisation)
        self.current_frame = 0
        self.max_frames = iterations * epochs - 1
        self.speed = 100

        self.iteration = iterations
        self.epochs = epochs
        self.current_algorithm_img = None
        self.current_average_img = None

        self.initUI()
        self.load_frame(0)

    def initUI(self):
        self.setStyleSheet("""
            background-color: #ECE9E9;
            color: black;
        """)

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.navbar = self.create_navbar("Visualisation")
        layout.addWidget(self.navbar)

        content_layout = QVBoxLayout()
        content_layout.setContentsMargins(0, 20, 0, 0)
        content_layout.setSpacing(15)

        vis_row = QHBoxLayout()
        vis_row.setSpacing(15)

        algorithm_frame = self.create_visualisation_frame("Algorithm visualisation")
        vis_row.addWidget(algorithm_frame, stretch=1)

        fitness_frame = self.create_visualisation_frame("Average Fitness Func value")
        vis_row.addWidget(fitness_frame, stretch=1)

        content_layout.addLayout(vis_row)

        timeline = QFrame()
        timeline.setStyleSheet("background-color: transparent;")

        timeline_layout = QHBoxLayout()
        self.timeline_slider = QSlider(Qt.Orientation.Horizontal)
        self.timeline_slider.setRange(0, self.max_frames)
        self.timeline_slider.setValue(0)
        self.timeline_slider.setStyleSheet("""
            QSlider::groove:horizontal {
                height: 4px;
                background: #a6a6a6;
            }
            QSlider::handle:horizontal {
                width: 12px;
                height: 12px;
                margin: -4px 0;
                border-radius: 6px;
                background: black;
            }
        """)
        self.timeline_slider.valueChanged.connect(self.slider_changed)
        timeline_layout.addWidget(self.timeline_slider)
        timeline.setLayout(timeline_layout)
        content_layout.addWidget(timeline)

        controls_layout = QHBoxLayout()
        controls_layout.setSpacing(15)

        media_controls = QHBoxLayout()
        media_controls.setSpacing(5)

        first_btn = QPushButton("|<")
        first_btn.setToolTip("Go to first iteration")
        first_btn.clicked.connect(self.go_to_first)

        prev_btn = QPushButton("<")
        prev_btn.setToolTip("Previous iteration")
        prev_btn.clicked.connect(self.go_to_previous)

        self.play_btn = QPushButton("Play")
        self.play_btn.setToolTip("Play")
        self.play_btn.clicked.connect(self.start_visualisation)

        next_btn = QPushButton(">")
        next_btn.setToolTip("Next iteration")
        next_btn.clicked.connect(self.go_to_next)

        last_btn = QPushButton(">|")
        last_btn.setToolTip("Go to last iteration")
        last_btn.clicked.connect(self.go_to_last)

        for button in [first_btn, prev_btn, self.play_btn, next_btn, last_btn]:
            button.setStyleSheet("""
                QPushButton {
                    background-color: rgba(146, 231, 173, 1);
                    color: rgba(0, 0, 0, 1);
                    font-family: Inter;
                    font-weight: bold;
                    font-size: 20px;
                    min-width: 60px;
                    border-radius: 5px;
                    border: none;
                    margin-bottom: 5px;
                    margin-left: 5px;
                }
                QPushButton:hover {
                    background-color: #01b522;
                }
            """)
            button.setFixedHeight(50)

        media_controls.addWidget(first_btn)
        media_controls.addWidget(prev_btn)
        media_controls.addWidget(self.play_btn)
        media_controls.addWidget(next_btn)
        media_controls.addWidget(last_btn)

        speed_layout = QHBoxLayout()
        speed_layout.setSpacing(5)

        speed_label = QLabel("Speed (ms):")
        speed_label.setFixedWidth(120)
        speed_label.setStyleSheet("color: black; margin-bottom: 10px; margin-right: 5px; font-size: 20px;")

        self.speed_input = QLineEdit(str(self.speed))
        self.speed_input.setFixedWidth(70)
        self.speed_input.setValidator(QIntValidator(1, 10000))
        self.speed_input.setStyleSheet("background-color: white; color: black; margin-bottom: 10px; font-size: 20px;")
        self.speed_input.textChanged.connect(self.update_speed)

        speed_layout.addWidget(speed_label)
        speed_layout.addWidget(self.speed_input)

        goto_layout = QHBoxLayout()
        goto_layout.setSpacing(5)

        goto_label = QLabel("Go to iteration:")
        goto_label.setStyleSheet("color: black; margin-bottom: 10px; margin-right: 5px; padding-right: 5px; font-size: 20px;")

        self.goto_input = QLineEdit()
        self.goto_input.setFixedWidth(50)
        self.goto_input.setValidator(QIntValidator(1, self.iteration))
        self.goto_input.setStyleSheet("background-color: white; color: black; margin-bottom: 10px; margin-right: 5px; font-size: 20px;")

        goto_btn = QPushButton("Go")
        goto_btn.setStyleSheet("""
            QPushButton {
                    background-color: rgba(146, 231, 173, 1);
                    color: rgba(0, 0, 0, 1);
                    font-family: Inter;
                    font-weight: bold;
                    font-size: 20px;
                    border-radius: 5px;
                    border: none;
                    margin-bottom: 5px;
            }
            QPushButton:hover {
                background-color: #01b522;
            }
        """)
        goto_btn.clicked.connect(self.go_to_specific_iteration)

        goto_layout.addWidget(goto_label)
        goto_layout.addWidget(self.goto_input)
        goto_layout.addWidget(goto_btn)

        controls_layout.addLayout(media_controls)
        controls_layout.addLayout(speed_layout)
        controls_layout.addStretch()
        controls_layout.addLayout(goto_layout)

        content_layout.addLayout(controls_layout)
        layout.addLayout(content_layout)
        self.setLayout(layout)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.update_images()

    def update_images(self):
        if self.current_algorithm_img and not self.current_algorithm_img.isNull():
            self.algorithm_label.setPixmap(self.current_algorithm_img.scaled(
                self.algorithm_label.size(),
                Qt.AspectRatioMode.KeepAspectRatio
            ))

        if self.current_average_img and not self.current_average_img.isNull():
            self.average_label.setPixmap(self.current_average_img.scaled(
                self.average_label.size(),
                Qt.AspectRatioMode.KeepAspectRatio
            ))

    def update_speed(self):
        try:
            self.speed = int(self.speed_input.text())
            if self.timer.isActive():
                self.timer.setInterval(self.speed)
        except ValueError:
            pass

    def go_to_first(self):
        self.timeline_slider.setValue(0)

    def go_to_last(self):
        self.timeline_slider.setValue(self.max_frames)

    def go_to_previous(self):
        if self.current_frame > 0:
            self.timeline_slider.setValue(self.current_frame - 1)

    def go_to_next(self):
        if self.current_frame < self.max_frames:
            self.timeline_slider.setValue(self.current_frame + 1)

    def go_to_specific_iteration(self):
        try:
            value = int(self.goto_input.text())
            if 1 <= value <= self.iteration:
                self.timeline_slider.setValue((value-1) * self.epochs)
        except ValueError:
            pass

    def start_visualisation(self):
        if not self.timer.isActive():
            self.timer.start(self.speed)
            self.play_btn.setText("Pause")
            self.play_btn.setToolTip("Pause")
            self.play_btn.clicked.disconnect()
            self.play_btn.clicked.connect(self.pause_visualisation)

    def pause_visualisation(self):
        if self.timer.isActive():
            self.timer.stop()
            self.play_btn.setText("Play")
            self.play_btn.setToolTip("Play")
            self.play_btn.clicked.disconnect()
            self.play_btn.clicked.connect(self.start_visualisation)

    def update_visualisation(self):
        if self.current_frame < self.max_frames:
            self.current_frame += 1
            self.timeline_slider.setValue(self.current_frame)
        else:
            self.pause_visualisation()

    def slider_changed(self, value):
        self.current_frame = value
        self.goto_input.setText(str(value//self.epochs+1))
        self.load_frame(value)

    def load_frame(self, frame_num):
        self.current_algorithm_img = QPixmap(f'./frames/algorithm_{frame_num}.jpg')
        self.current_average_img = QPixmap(f'./frames/average_fitness_{frame_num}.jpg')
        self.update_images()

    def create_visualisation_frame(self, title):
        frame = QFrame()
        frame.setStyleSheet("""
            background-color: #ECE9E9;
            border-radius: 5px;
            padding: 10px;
        """)
        frame.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        layout = QVBoxLayout()
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(10)

        title_label = QLabel(title)
        title_label.setStyleSheet("""
            font-family: 'Inter';
            font-weight: bold;
            color: #000000;
            font-size: 28px;
            margin-bottom: 5px;
        """)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        content = QLabel()
        content.setStyleSheet("background-color: #ffffff;")
        content.setMinimumHeight(450)
        content.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        if "Algorithm" in title:
            self.algorithm_label = content
        else:
            self.average_label = content

        layout.addWidget(title_label)
        layout.addWidget(content)
        frame.setLayout(layout)

        return frame

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