from nicegui import ui
from task import getTask, Task

from nicegui import app

app.add_static_files('/static', 'static')

def start_sim(mode, task):
    print(f'Starte {task} im Modus: {mode}')


tasks = ['Place Cube', 'Insertion', 'Build Pyramid']
selected_task = {'value': 'Place Cube'}
task_buttons = {}

start_view = ui.column().classes('items-center justify-center h-screen w-full')
with start_view:
    # ui.label('Wähle eine Aufgabe').classes('text-3xl mb-8')
    with ui.row().classes('w-full justify-around'):
        for task in tasks:
            btn = ui.button(task).classes(
                'h-40 text-2xl grow bg-gray-100 text-gray-700 rounded-xl hover:bg-gray-200')
            btn.on('click', lambda e, t=task: show_task_view(t))
            task_buttons[task] = btn
    ui.separator().style('width: 100%; height: 2px; background-color: #f3f4f6; margin-top: 10px;')

task_view = ui.column().classes('p-8 hidden')
camera_view = ui.column().classes('p-8 hidden')


def show_task_view(task):
    selected_task['value'] = task
    start_view.classes(remove='items-center h-screen')
    task_view.classes(remove='hidden')
    camera_view.classes(remove='hidden')

    task_view.clear()
    with task_view:
        task_obj: Task = getTask(task)
        ui.label(task_obj.title).classes('text-5xl font-bold')
        with ui.row():
            with ui.column().style('flex:1'):
                ui.label(task_obj.description).classes('text-2xl')
            with ui.column().style('flex:1'):
                ui.image(f'/static/proxy-image.png').classes('max-w-full')

        with ui.row().classes('mt-4 w-full'):
            ui.label("Task Difficulty").classes('text-5xl font-bold')
        with ui.row().classes('mt-4 w-full'):
            ui.label("There are different difficulty levels for this task. Choose one!").classes('text-2xl')
        with ui.row().classes('mt-4 w-full'):
            ui.radio(task_obj.stages).classes('w-full text-2xl')
        with ui.row().classes('mt-4 w-full'):
            ui.label("AI-Model").classes('text-5xl font-bold')
        with ui.row().classes('mt-4 w-full'):
            ui.label("Choose a difficulty level that the AI model is trained for.").classes('text-2xl')
        with ui.row().classes('mt-4 w-full'):
            ui.radio(task_obj.stages).classes('w-full text-2xl')

    with camera_view:
        # add camera stream
        cameras = ["wrist_cam_right", "wrist_cam_left", "overhead_cam", "worms_eye_cam"]
        for cam in cameras:
            ui.image(f'http://localhost:5000/video_feed?cam={cam}').style('width: 640px; height: 480px; object-fit: cover;')

ui.run()
