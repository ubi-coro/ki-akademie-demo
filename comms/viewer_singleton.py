from comms.sim_viewer import MujocoStreamViewer


viewer = None
def get_viewer():
    global viewer
    if viewer is None:
        viewer = MujocoStreamViewer(model=None, data=None)
    return viewer