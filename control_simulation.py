from lerobot.common.robot_devices.control_configs import SimControlPipelineConfig, TeleoperateControlConfig, \
    PolicyControlConfig
from lerobot.common.robot_devices.robots.configs import GellohaConfig
from lerobot.common.sim.configs import AlohaSimConfig
from lerobot.configs.policies import PreTrainedConfig
from lerobot.scripts.control_sim_robot import control_sim_robot

import threading

from comms.viewer_singleton import get_viewer
from comms.stream_server import start_flask
from comms import sim_viewer
from task import TaskName


def run_teleop(task_name, stage, stop_event):
    threading.Thread(target=start_flask, daemon=True).start()
    sim = AlohaSimConfig()
    sim.viewer = "mujoco_stream"
    sim.task_name = get_env_task_name(task_name, stage)
    robot = GellohaConfig()
    control = TeleoperateControlConfig()
    cfg = SimControlPipelineConfig(sim=sim, robot=robot, control=control)

    control_sim_robot(cfg, stop_event)
    print("DONE TELEOP")


def run_policy(task_name, stage, model, stop_event):
    threading.Thread(target=start_flask, daemon=True).start()
    sim = AlohaSimConfig()
    sim.viewer = "mujoco_stream"
    sim.task_name = get_env_task_name(task_name, stage)
    robot = GellohaConfig()
    policy_path = get_policy_path(task_name, model)
    control = PolicyControlConfig(
        repo_id="jzilke/act_policy",
        single_task=task_name,
    )
    control.policy = PreTrainedConfig.from_pretrained(policy_path)
    control.policy.pretrained_path = policy_path
    cfg = SimControlPipelineConfig(sim=sim, robot=robot, control=control)
    control_sim_robot(cfg, stop_event)
    print("DONE POLICY")

def get_env_task_name(task_name: str, stage: int):
    if task_name == TaskName.BUILD_PYRAMID:
        return "stacking"
    elif task_name == TaskName.INSERTION:
        return "insertion"
    elif task_name == TaskName.PLACE_CUBE and stage == "stage 1":
        return  "place_cube_0"
    elif task_name == TaskName.PLACE_CUBE and stage == "stage 2":
        return  "place_cube_1"
    else:
        return  "place_cube_2"


def get_policy_path(task_name, model):
    if task_name == TaskName.BUILD_PYRAMID:
        r =  "/media/local/outputs/train/stacking_jonas/checkpoints/006000/pretrained_model"
    elif task_name == TaskName.INSERTION:
        r =  "/media/local/outputs/train/insertion_new/checkpoints/last/pretrained_model"
    elif task_name == TaskName.PLACE_CUBE and model == "stage 1":
        r =  "/media/local/outputs/train/stage_0/checkpoints/last/pretrained_model"
    elif task_name == TaskName.PLACE_CUBE and model == "stage 2":
        r =  "/media/local/outputs/train/stage_1/checkpoints/last/pretrained_model"
    else:
        r =  "/media/local/outputs/train/stage_2/checkpoints/last/pretrained_model"
    print()
    print(f"Policy path: {r}")
    return r