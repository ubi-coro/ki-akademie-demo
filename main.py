from nicegui import app, ui
from views import start_view, task_view, camera_view, build_start_view

app.add_static_files('/static', 'static')

build_start_view()

ui.run()