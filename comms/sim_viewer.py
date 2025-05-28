import cv2
from lerobot.common.sim.viewer import AbstractViewer
from comms.global_frame import set_current_frame, frame_lock
import mujoco.viewer

@AbstractViewer.register_subclass("stream")
class StreamViewer(AbstractViewer):
    def __init__(self, image_keys=None, **kwargs):
        self.image_keys = image_keys
        self.running = False

    def start(self):
        self.running = True

    def stop(self):
        cv2.destroyAllWindows()
        self.running = False

    def is_running(self):
        return self.running

    def sync(self, observation):
        if not self.image_keys:
            self.image_keys = list(observation['pixels'].keys())
        for key in self.image_keys:
            image = observation['pixels'][key].squeeze(0)
            image_bgr = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            _, jpeg = cv2.imencode('.jpg', image_bgr)
            set_current_frame(key, jpeg.tobytes())

@AbstractViewer.register_subclass("mujoco_stream")
class MujocoStreamViewer(AbstractViewer):
    def __init__(self, model, data, image_keys=None, **kwargs):
        self.model = model
        self.data = data
        self.viewer = None
        self.image_keys = image_keys
        self.running = False



    def start(self):
        if not self.is_running():
            self.viewer = mujoco.viewer.launch_passive(self.model, self.data, show_left_ui=False, show_right_ui=False)
            self.viewer.user_scn.flags[mujoco.mjtRndFlag.mjRND_SHADOW] = 0
            self.viewer.user_scn.flags[mujoco.mjtRndFlag.mjRND_REFLECTION] = 0
            self.viewer.user_scn.flags[mujoco.mjtRndFlag.mjRND_SKYBOX] = 0
            self.viewer.user_scn.flags[mujoco.mjtRndFlag.mjRND_HAZE] = 0
            self.viewer.user_scn.flags[mujoco.mjtRndFlag.mjRND_CULL_FACE] = 0
            # self.viewer.__enter__()

    def stop(self):
        if self.viewer is not None:
            self.viewer.close()
            self.viewer = None

    def is_running(self):
        return self.viewer.is_running() if self.viewer else False

    def sync(self, observation):
        if self.viewer:
            self.viewer.sync()
        for key in self.image_keys:
            image = observation['pixels'][key].squeeze(0)
            image_bgr = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            _, jpeg = cv2.imencode('.jpg', image_bgr)
            set_current_frame(key, jpeg.tobytes())
