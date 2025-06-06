import tkinter as tk
try:
    from ctypes import windll
    windll.shcore.SetProcessDpiAwareness(1)
except ImportError:
    print("Error: windll not imported. Text may be blurred")
    pass

from app.gui.components.html_component_editor import HtmlComponentEditor
from app.util.controller import JsonController, Controller
colors = JsonController.get_config_data("colors")
C1 = colors["c1"]
C2 = colors["c2"]
C3 = colors["c3"]
C4 = colors["c4"]

POST_COMPONENT_PATH = Controller.get_resource_paths("html_post_folder")

class ConfigPost(tk.Frame):
    def __init__(self, container):
        super().__init__(container)
        self.config(bg=C1)
        #GROUPER FRAMES
        body = tk.Frame(self, bg="red")
        body.pack()
        
        component_editor = HtmlComponentEditor(body, POST_COMPONENT_PATH, "post")
        component_editor.pack()
