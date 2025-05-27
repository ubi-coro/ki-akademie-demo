from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QFormLayout, QComboBox, QPushButton,
    QHBoxLayout, QSizePolicy, QRadioButton, QButtonGroup, QGroupBox, QSlider
)
from enum import Enum

lorem_ipsum = ("""
Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.
Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.
Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.
Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.
""")

# --- Styles ---
RADIO_STYLE = """
    font-size: 12pt;
    padding: 6px 12px;
    background-color: #ffffff;
    border-radius: 6px;
    color: #2c3e50;
"""

DESC_STYLE = "font-size: 26pt; color: white; padding: 12px;"
VIDEO_STYLE = """
    background-color: #34495e;
    color: white;
    font-size: 16pt;
    border-radius: 10px;
"""
CONTAINER_STYLE = """
    QGroupBox {
        border: 1px solid #ccc;
        border-radius: 8px;
        margin-top: 65px; /* space for the title */
        font: 30pt 'Segoe UI';
    }
    QGroupBox::title {
        subcontrol-origin: margin;
        subcontrol-position: top left;
        padding: 0 8px;
        background-color: transparent;
        font: bold 30pt 'Segoe UI';
    }
"""
START_BTN_STYLE = """
    background-color: #2980b9;
    color: white;
    font-weight: bold;
    font-size: 18pt;
    border-radius: 10px;
"""
RADIO_BUTTON_STYLE = """
    QRadioButton::indicator {
        width: 15px; height: 15px; border-radius: 7px;
        border: 2px solid white; background-color: transparent;
    }
    QRadioButton::indicator:checked {
        background-color: white;
        border: 2px solid white;
    }
"""


class Difficulty(Enum):
    EASY = "Easy"
    MEDIUM = "Medium"
    HARD = "Hard"


class InsertionTab(QWidget):
    def __init__(self):
        super().__init__()
        self.difficulty_group = QButtonGroup()

        main_layout = QVBoxLayout(self)
        main_layout.addLayout(self.create_desc_and_video())
        main_layout.addLayout(self.create_settings_split())
        main_layout.addStretch()
        main_layout.addWidget(self.create_start_buttons())

    def create_desc_and_video(self):
        layout = QHBoxLayout()

        desc = QLabel("Greife den roten Stab und positioniere ihn genau auf dem Ziel, das durch einen blauen Kreis dargestellt wird.")
        desc.setWordWrap(True)
        desc.setStyleSheet(DESC_STYLE)
        desc.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)

        video = QLabel("Video Player Placeholder")
        video.setAlignment(Qt.AlignmentFlag.AlignCenter)
        video.setStyleSheet(VIDEO_STYLE)
        video.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        video.setMinimumHeight(270 * 2)

        layout.addWidget(desc, 1)
        layout.addWidget(video, 1)
        return layout

    def create_settings_split(self):
        layout = QHBoxLayout()

        font = QFont()
        font.setPointSize(25)  # Increase font size

        # Simulation Environment Settings
        env_group = QGroupBox("Simulation Environment Settings")
        env_group.setStyleSheet(CONTAINER_STYLE)
        env_group.setFont(font)
        env_layout = QVBoxLayout()
        env_buttons = QButtonGroup(env_group)
        for i, option in enumerate(["Option 1", "Option 2", "Option 3"]):
            rb = QRadioButton(option)
            rb.setStyleSheet(RADIO_BUTTON_STYLE)
            rb.setFont(font)
            env_layout.addWidget(rb)
            env_buttons.addButton(rb, i)
        env_group.setLayout(env_layout)

        # Trained Policy Settings
        policy_group = QGroupBox("Trained Policy Settings")
        policy_group.setStyleSheet(CONTAINER_STYLE)
        policy_group.setFont(font)
        policy_layout = QVBoxLayout()
        policy_buttons = QButtonGroup(policy_group)
        for i, option in enumerate(["Option A", "Option B", "Option C"]):
            rb = QRadioButton(option)
            rb.setFont(font)
            rb.setStyleSheet(RADIO_BUTTON_STYLE)
            policy_layout.addWidget(rb)
            policy_buttons.addButton(rb, i)
        policy_group.setLayout(policy_layout)

        layout.addWidget(env_group, 1)
        layout.addWidget(policy_group, 1)
        return layout

    def create_start_buttons(self):
        container = QWidget()
        layout = QHBoxLayout(container)

        btn_start = QPushButton("Start Simulation")
        btn_start.setFixedHeight(150)
        btn_start.setStyleSheet(START_BTN_STYLE)
        btn_start.clicked.connect(self.on_start)

        btn_teleop = QPushButton("Teleoperation")
        btn_teleop.setFixedHeight(150)
        btn_teleop.setStyleSheet(START_BTN_STYLE)
        # Connect btn_teleop.clicked to the corresponding handler if any

        layout.addWidget(btn_start)
        layout.addWidget(btn_teleop)
        return container

    def get_selected_difficulty(self):
        for btn in self.difficulty_group.buttons():
            if btn.isChecked():
                return btn.text()

    def on_start(self):
        selected = self.get_selected_difficulty()
        print(f"Starting simulation with difficulty: {selected}")
