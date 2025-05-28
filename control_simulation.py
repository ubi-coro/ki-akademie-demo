from lerobot.common.robot_devices.control_configs import SimControlPipelineConfig, TeleoperateControlConfig
from lerobot.common.robot_devices.robots.configs import GellohaConfig
from lerobot.common.sim.configs import AlohaSimConfig
from lerobot.scripts.control_sim_robot import control_sim_robot

import threading
from comms.stream_server import start_flask
from comms import sim_viewer


def run_teleop(task_name, stage, stop_event):
    threading.Thread(target=start_flask, daemon=True).start()
    sim = AlohaSimConfig()
    sim.viewer = "stream"
    sim.task_name = get_env_task_name(task_name, stage)
    robot = GellohaConfig()
    control = TeleoperateControlConfig()
    cfg = SimControlPipelineConfig(sim=sim, robot=robot, control=control)
    control_sim_robot(cfg, stop_event)



def get_env_task_name(task_name: str, stage: int):
    if task_name == "Build Pyramid":
        return "stacking"
    elif task_name == "Insertion":
        return "insertion"
    elif task_name == "Place Cube" and stage == 0:
        return  "place_cube_0"
    elif task_name == "Place Cube" and stage == 1:
        return  "place_cube_1"
    else:
        return  "place_cube_2"

