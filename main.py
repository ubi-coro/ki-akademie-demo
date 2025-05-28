from nicegui import app, ui
from start_page import start_site
from views import build_start_view

app.add_static_files('/static', 'static')

ui.add_head_html('''
<style>
  html, body, #app, main, .q-layout, .q-page-container, .nicegui-content {
    padding: 0 !important;
  }
  
  .q-page-container {
  margin-top: 0 !important;
  padding-top: 0 !important;
  height: 100% !important;
}

  html.dark, body.dark, .q-body.dark {
    background-color: #3a3a3a !important;
  }

  .custom-header {
    background-color: #4a4a4a !important;
    height: 100px !important;
    min-height: 100px !important;
    margin: 0 !important;
    padding: 0 32px !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    width: 100% !important;
  }

  .q-header, .q-header__container {
    margin: 0 !important;
    padding: 0 !important;
    height: 100px !important;
    min-height: 100px !important;
    background-color: transparent !important;
  }

  body > div:first-child {
    margin-top: 0 !important;
    padding-top: 0 !important;
  }
</style>
''')

# start_site()
build_start_view()

ui.run(dark=True)
