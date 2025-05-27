import cv2
from lerobot.common.sim.viewer import AbstractViewer
from comms.global_frame import set_current_frame, frame_lock

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