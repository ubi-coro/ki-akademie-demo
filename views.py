import threading

from nicegui import ui

from control_simulation import run_teleop
from tasks import tasks, getTask, Task

selected_task = {'value': 'Place Cube'}

start_view = ui.column().classes('items-center justify-center h-screen w-full')
task_view = ui.column().classes('p-8 hidden')
camera_view = ui.column().classes('p-8 hidden')

camera_shown = {'value': False}
teleop_thread = None
stop_event = None

def handle_teleop(task: str, stage: str):
    global teleop_thread, stop_event

    # Stop current simulation if running
    if teleop_thread and teleop_thread.is_alive():
        print("Stopping existing teleop")
        stop_event.set()
        teleop_thread.join()

    # Start new simulation
    stop_event = threading.Event()
    teleop_thread = threading.Thread(
        target=run_teleop,
        args=(task, stage, stop_event),
        daemon=True
    )
    teleop_thread.start()

    if not camera_shown['value']:
        camera_view.classes(remove='hidden')
        camera_shown['value'] = True

def handle_ai_model(task: str, stage: str, ai_model: str):
    print(f"AI model execution started {task, stage, ai_model}")

def show_task_view(task):
    selected_task['value'] = task
    start_view.classes(remove='items-center h-screen')
    task_view.classes(remove='hidden')
    camera_view.classes(remove='hidden')
    task_view.clear()
    camera_view.clear()

    task_obj: Task = getTask(task)

    with task_view:
        with ui.column().style('width: 800px; margin-right: 100px;'):
            ui.label(task_obj.title).classes('text-5xl font-bold')
            ui.label(task_obj.description).classes('text-2xl')
            ui.image(f'/static/proxy-image.png').classes('max-w-full mt-4')

            ui.label("Task Difficulty").classes('text-5xl font-bold mt-8')
            ui.label("There are different difficulty levels for this task. Choose one!").classes('text-2xl')
            stage_radio = ui.radio(task_obj.stages, value='stage 1').classes('text-2xl')

            ui.label("AI-Model").classes('text-5xl font-bold mt-8')
            ui.label("Choose a difficulty level that the AI model is trained for.").classes('text-2xl')
            ai_radio = ui.radio(task_obj.stages, value='stage 1').classes('text-2xl')

            with ui.row().classes('mt-6 gap-4'):
                ui.button('Start Teleoperation', on_click=lambda: handle_teleop(task, stage_radio.value)).classes(
                    'w-full text-xl px-6 py-2')
                ui.button('Run AI Model', on_click=lambda: handle_ai_model(task, stage_radio.value, ai_radio.value)).classes(
                    'w-full text-xl px-6 py-2')

    with camera_view:
        ui.label("Camera View").classes('text-5xl font-bold')
        with ui.row():
            with ui.column().style('flex:1'):
                for cam in ["wrist_cam_left", "worms_eye_cam"]:
                    ui.image(f'http://localhost:5000/video_feed?cam={cam}').style(
                        'width: 768px; height: 576px; object-fit: cover; margin-bottom: 10px;')
            with ui.column().style('flex:1'):
                for cam in ["wrist_cam_right", "overhead_cam"]:
                    ui.image(f'http://localhost:5000/video_feed?cam={cam}').style(
                        'width: 768px; height: 576px; object-fit: cover; margin-bottom: 10px;')

def build_start_view():
    with start_view:
        with ui.row().classes('w-full justify-around'):
            for task in tasks:
                btn = ui.button(task).classes(
                    'h-40 text-2xl grow bg-gray-100 text-gray-700 rounded-xl hover:bg-gray-200')
                btn.on('click', lambda e, t=task: show_task_view(t))
    ui.separator().style('width: 100%; height: 2px; background-color: #f3f4f6; margin-top: 10px;')

    # Layout both views side-by-side at startup
    with ui.row().classes('w-full'):
        global task_view, camera_view
        task_view = ui.column().classes('p-8 hidden').style('flex: 1')
        camera_view = ui.column().classes('p-8 hidden').style('flex: 4')


# ui.run()
