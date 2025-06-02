import threading

from nicegui import ui

from control_simulation import run_teleop, run_policy
from task import tasks, getTask, Task, TaskName

selected_task = {'value': 'Place Cube'}

custom_header = ui.header().classes('custom-header')
start_view = ui.column().classes('items-center w-full')
tele_operator_view = ui.column().classes('p-8 hidden')
task_view = ui.row().classes('p-8')
information_view = ui.row().classes('p-8')
camera_view = ui.column().classes('hidden')

camera_shown = {'value': False}
teleop_thread = None
stop_event = None


def handle_teleop(task: str, stage: str):
    global teleop_thread, stop_event
    # Start new simulation
    stop_event = threading.Event()
    teleop_thread = threading.Thread(
        target=run_teleop,
        args=(task, stage, stop_event),
        daemon=True
    )
    teleop_thread.start()
    print(f"teleop thread: {teleop_thread}")

    if not camera_shown['value']:
        camera_view.classes(remove='hidden')
        camera_shown['value'] = True

    show_viewer()


def handle_ai_model(task: str, stage: str, ai_model: str):
    global teleop_thread, stop_event
    print(f"Task: {task}, Stage: {stage}, AIModel: {ai_model}")
    stop_event = threading.Event()
    teleop_thread = threading.Thread(
        target=run_policy,
        args=(task, stage, ai_model, stop_event),
        daemon=True
    )
    teleop_thread.start()
    print(f"teleop thread: {teleop_thread}")
    if not camera_shown['value']:
        camera_view.classes(remove='hidden')
        camera_shown['value'] = True

    show_viewer()




def end_task():
    global teleop_thread, stop_event
    print("END TASK")
    # Stop current simulation if running
    if teleop_thread and teleop_thread.is_alive():
        print("Stopping existing teleop")
        stop_event.set()
        teleop_thread.join()
    else:
        print(f"teleop thread: {teleop_thread}")
        print(f"teleop thread alive: {teleop_thread.is_alive()}")
        print("didnt stop")
    camera_view.classes('hidden')
    tele_operator_view.classes('hidden')
    start_view.classes(remove='hidden')
    show_header()
    show_task_view(selected_task['value'])


def show_task_view(task):
    selected_task['value'] = task


    task_view.classes(remove='hidden')
    information_view.classes('hidden')
    camera_view.classes('hidden')
    tele_operator_view.classes('hidden')
    task_view.clear()

    task_obj: Task = getTask(task)

    if task == TaskName.PLACE_CUBE:
        show_pick_and_place_view(task_obj)

    elif task == TaskName.BUILD_PYRAMID:
        show_tower_stacking(task_obj)
    elif task == TaskName.INSERTION:
        show_insertion(task_obj)


def show_pick_and_place_view(task_obj: Task):
    with task_view:
        with ui.column().style('width: 1400px; padding-right: 400px;'):
            ui.label(task_obj.title).classes('text-5xl font-bold')
            ui.label(task_obj.description).classes('text-2xl')

            ui.label("Your Task").classes('text-5xl font-bold mt-8').style('margin-topt: 25px;')
            ui.label(task_obj.user_task).classes('text-2xl')

            ui.label("Task Difficulty").classes('text-5xl font-bold mt-8')
            ui.label("There are different difficulty levels for this task. Choose one!").classes('text-2xl')
            stage_radio = ui.radio(task_obj.stages, value='stage 1').classes('text-2xl')

            ui.label("AI-Model").classes('text-5xl font-bold mt-8')
            ui.label("Choose data that the AI model is trained for.").classes('text-2xl')
            ai_radio = ui.radio(task_obj.stages, value='stage 1').classes('text-2xl')
        with ui.column().style('width: 1600px;'):
            ui.image(task_obj.image_path).classes('mt-4')
        with ui.row().classes('mt-6 gap-4'):
            ui.button('Start Teleoperation', on_click=lambda: handle_teleop(task_obj.title, '')).classes(
                'w-80 text-xl px-6 py-2')
            ui.button('Run AI Model',
                      on_click=lambda: handle_ai_model(task_obj.title, '', '')).classes(
                'w-80 text-xl px-6 py-2')


def show_tower_stacking(task_obj: Task):
    with task_view:
        with ui.column().style('width: 1400px; padding-right: 400px;'):
            ui.label(task_obj.title).classes('text-5xl font-bold')
            ui.label(task_obj.description).classes('text-2xl')

            ui.label("Your Task").classes('text-5xl font-bold mt-8')
            ui.label(task_obj.user_task).classes('text-2xl')


        with ui.column().style('width: 1600px;'):
            ui.image(task_obj.image_path).classes('mt-4')
        with ui.row().classes('mt-6 gap-4'):
            ui.button('Start Teleoperation', on_click=lambda: handle_teleop(task_obj.title, '')).classes(
                'w-80 text-xl px-6 py-2')
            ui.button('Run AI Model',
                      on_click=lambda: handle_ai_model(task_obj.title, '', '')).classes(
                'w-80 text-xl px-6 py-2')


def show_insertion(task_obj: Task):
    with task_view:
        with ui.column().style('width: 1400px; padding-right: 400px;'):
            ui.label(task_obj.title).classes('text-5xl font-bold')
            ui.label(task_obj.description).classes('text-2xl')

            ui.label("Your Task").classes('text-5xl font-bold mt-8')
            ui.label(task_obj.user_task).classes('text-2xl')

        with ui.column().style('width: 1600px;'):
            ui.image(task_obj.image_path).classes('mt-4')
        with ui.row().classes('mt-6 gap-4'):
            ui.button('Start Teleoperation', on_click=lambda: handle_teleop(task_obj.title, '')).classes(
                'w-80 text-xl px-6 py-2')
            ui.button('Run AI Model',
                      on_click=lambda: handle_ai_model(task_obj.title, '', '')).classes(
                'w-80 text-xl px-6 py-2')

def show_viewer():
    global custom_header
    start_view.classes('hidden')
    task_view.classes('hidden')
    custom_header.classes('hidden')
    custom_header.clear()
    custom_header.style('display: none;')

    tele_operator_view.classes(remove='hidden')
    tele_operator_view.clear()

    camera_view.classes(remove='hidden')
    camera_view.clear()

    with tele_operator_view:
        # ui.label("Teleoperator View").classes('text-5xl font-bold')
        # ui.image('http://localhost:5000/video_feed?cam=teleoperator_pov').style(
        #     'width: 80%; object-fit: cover; margin-bottom: 10px;')
        ui.button('End Task', on_click=lambda: end_task()).classes(
            'w-full text-xl px-6 py-2').style('margin-top: 1300px')
    with camera_view:
        # ui.label("Camera View").classes('text-4xl font-bold').style('margin-top: 0px')
        with ui.column().style('flex:1'):
            for cam in ["wrist_cam_left", "worms_eye_cam", "wrist_cam_right", "overhead_cam"]:
                ui.image(f'http://localhost:5000/video_feed?cam={cam}').style(

                    'width: 450px; height: 337px; object-fit: cover; margin-bottom: 10px; margin-top: 0px;')

def show_header():
    custom_header.style('display: flex;')
    custom_header.classes(remove='hidden')
    custom_header.clear()
    with custom_header:
        ui.label("Human Demonstrates, Robot Learns: Imitation via Teleoperation").classes(
            'text-7xl font-bold text-white text-center w-full').style('margin-top: 15px;')
        ui.separator().style('width: 100%; height: 2px; background-color: #f3f4f6; margin-top: 0px; margin-bottom: 10px;')


def show_information():
    information_view.classes(remove='hidden')

    task_view.classes('hidden')
    camera_view.classes('hidden')
    tele_operator_view.classes('hidden')
    information_view.clear()

    with information_view:
        with ui.column().style('width: 1400px;'):
            ui.label("AI Model").classes('text-6xl font-bold')


            with ui.list().classes('list-disc ml-6 text-base'):
                ui.html("<li><b>Architecture:</b> Action Chunking Transformer</li>").classes('text-3xl').style('margin-top: 18px;')
                ui.html("<li><b>Behavior Cloning:</b> Only supervised, offline learning</li>").classes('text-3xl').style('margin-top: 18px;')
                ui.html("<li><b>Input:</b> 4 cameras images (480x640x3) and current robot state (2 x 7 Joints)</li>").classes('text-3xl').style('margin-top: 18px;')
                ui.html("<li><b>Output:</b>  30-step action sequences (1 second)</li>").classes('text-3xl').style('margin-top: 18px;')
                ui.html("<li><b>Stateless:</b> no temporal history, only single-step inference.</li>").classes('text-3xl').style('margin-top: 18px;')

            ui.label("Data Collection via Teleoperation").classes('text-6xl font-bold').style('margin-top: 25px;')

            with ui.list().classes('list-disc ml-6 text-base'):
                ui.html("<li><b>Environment:</b> MuJoCo simulation</li>").classes('text-3xl').style('margin-top: 18px;')
                ui.html("<li><b>Teleoperation Tool:</b> Task executed using Gello</li>").classes('text-3xl').style(
                    'margin-top: 18px;')
                ui.html("<li><b>Tasks:</b> Learn 3 different Tasks</li>").classes('text-3xl').style('margin-top: 18px;')
                ui.html("<li><b>Dataset Size:</b> Approximately 50 episodes per task</li>").classes('text-3xl').style('margin-top: 18px;')

            ui.label("Problems").classes('text-6xl font-bold').style('margin-top: 25px;')

            with ui.list().classes('list-disc ml-6 text-base'):
                ui.html("<li><b>Out of Distribution:</b> mismatch between training and real-world data distributions.</li>").classes('text-3xl').style('margin-top: 18px;')
                ui.html("<li><b>Covariate shift</b></li>").classes('text-3xl').style('margin-top: 18px;')


        with ui.column().style('width: 1600px;'):
            ui.image("/static/architecture.png").classes('mt-4')


def build_start_view():
    show_header()

    with start_view:
        with ui.row().classes('w-full justify-around px-8 py-2'):
            btn = ui.button("Imitation Learning").props('flat').classes(
                'h-40 text-2xl grow bg-gray-500 text-black rounded-xl hover:bg-gray-600')
            btn.on('click', show_information)
            for task in tasks:
                btn = ui.button(task).classes(
                    'h-40 text-2xl grow bg-gray-100 text-gray-700 rounded-xl hover:bg-gray-200')
                btn.on('click', lambda e, t=task: show_task_view(t))


    # Layout both views side-by-side at startup
    with ui.row().classes('w-full'):
        global task_view, camera_view, tele_operator_view
        tele_operator_view = ui.column().classes('p-8 hidden').style('flex: 3')
        # task_view = ui.column().classes('p-8 hidden').style('flex: 1')
        camera_view = ui.column().classes('p-8 hidden').style('flex: 1')

    with ui.footer().classes('h-[160px] flex items-center justify-end gap-4 bg-white'):
        ui.image('/static/Universität_Bielefeld_Logo.svg').classes('h-[100px] w-[420px] object-contain')
        ui.image('/static/Logo-IOSB-INA.png').classes('h-[85px] w-[310px] object-contain')
        ui.image('/static/Ki_akademie.png').classes('h-[150px] w-[330px] object-contain')

        show_information()
