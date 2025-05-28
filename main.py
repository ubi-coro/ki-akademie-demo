from nicegui import app, ui
from views import build_start_view

app.add_static_files('/static', 'static')

ui.add_head_html('''
<style>
  html.dark, body.dark, .q-body.dark {
    background-color: #3a3a3a !important; /* more neutral dark gray */
  }
</style>
''')

build_start_view()



ui.run(dark=True)