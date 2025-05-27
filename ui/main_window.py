from PyQt6.QtWidgets import QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel, QComboBox, QHBoxLayout, QListWidget, \
    QTabWidget
from PyQt6.QtWidgets import QSizePolicy
from lerobot.common.policies.act.configuration_act import ACTConfig
from lerobot.common.robot_devices.control_configs import TeleoperateControlConfig, SimControlPipelineConfig, \
    RecordControlConfig
from lerobot.common.robot_devices.robots.configs import GellohaConfig
from lerobot.common.sim.configs import AlohaSimConfig
from lerobot.scripts.control_sim_robot import control_sim_robot

from ui.image_viewer import ImageViewer
from ui.insertion_tab import InsertionTab


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setup_window()
        self.setup_tabs()
        self.setup_controls()
        self.setup_layouts()

    def setup_window(self):
        self.setWindowTitle("Robot Demo UI")
        self.setGeometry(100, 100, 800, 600)

    def setup_tabs(self):
        self.tabs = QTabWidget()
        self.tabs.setStyleSheet("""
            QTabBar::tab {
                min-width: 1210px;
                min-height: 60px;
                background: #2c3e50;
                color: white;
                font: bold 30pt 'Segoe UI';
                padding: 16px 24px;
                border-top-left-radius: 12px;
                border-top-right-radius: 12px;
                margin-right: 4px;
                text-align: center;
            }
            QTabBar::tab:selected {
                background: #3498db;
                color: white;
            }
            QTabWidget::pane {
                border-top: 2px solid #3498db;
            }
        """)
        self.tabs.setTabPosition(QTabWidget.TabPosition.North)
        self.tabs.setMovable(False)


        self.tabs.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        self.tabs.addTab(InsertionTab(), "Insertion")
        self.tabs.addTab(QWidget(), "Place Cube")
        self.tabs.addTab(QWidget(), "Build Pyramid")
        self.tabs.currentChanged.connect(self.on_tab_changed)

        self.showMaximized()

    def update_controls_for_task(self, task):
        if task == "Build Pyramid":
            self.stage_combo.setVisible(True)
        else:
            self.stage_combo.setVisible(False)

    def on_tab_changed(self, index):
        task = self.tabs.tabText(index)
        self.update_controls_for_task(task)

    def setup_controls(self):
        self.mode_combo = QComboBox()
        self.mode_combo.addItems(["Teleoperation", "Policy"])
        self.mode_combo.currentTextChanged.connect(self.on_mode_changed)

        self.stage_combo = QComboBox()
        self.stage_combo.addItems(["Stage 0", "Stage 1", "Stage 2"])
        self.stage_combo.setVisible(False)

        self.button = QPushButton("Start Demo")
        self.button.clicked.connect(self.on_button_clicked)

        self.image_view = ImageViewer()

    def setup_layouts(self):
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.tabs)
        main_layout.addWidget(self.mode_combo)
        main_layout.addWidget(self.stage_combo)
        main_layout.addWidget(self.button)
        main_layout.addWidget(self.image_view)

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)


    def on_mode_changed(self, text):
        self.stage_combo.setVisible(text == "Policy")

    def on_task_changed(self, text):
        pass

    def on_button_clicked(self):
        pass
        # stage_str = self.stage_combo.currentText()
        # mode_str = self.mode_combo.currentText()
        # sim = AlohaSimConfig()
        # robot = GellohaConfig()
        # control = None
        # if mode_str == "Teleoperation":
        #     control = TeleoperateControlConfig()
        # elif mode_str == "Policy":
        #     repo_id = "jzilke/place_cube_policy"
        #     single_task = "Place Cube"
        #     control = RecordControlConfig(repo_id=repo_id, single_task=single_task)
        #     control.fps = 30
        #     control.episode_time_s = 180
        #     control.reset_time_s = 10
        #     policyConfig = ACTConfig()
        #     path = "/media/local/outputs/train/stage_1/checkpoints/010000/pretrained_model"
        #     policyConfig.pretrained_path = path
        #     policyConfig.device = "cuda:0"
        #     control.policy = policyConfig
        #     control.policy.path = "/media/local/outputs/train/stage_1/checkpoints/010000/pretrained_model"
        # cfg = SimControlPipelineConfig(sim=sim, robot=robot, control=control)
        #
        #
        # control_sim_robot(cfg)
