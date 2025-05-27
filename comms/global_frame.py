import threading

current_frames = {}
frame_lock = threading.Lock()

def set_current_frame(cam_id, frame_bytes):
    with frame_lock:
        current_frames[cam_id] = frame_bytes

def get_current_frame(cam_id):
    with frame_lock:
        return current_frames.get(cam_id, None)