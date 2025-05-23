import tkinter as tk
import shutil
import os
from bs4 import BeautifulSoup as bs
try:
    from ctypes import windll
    windll.shcore.SetProcessDpiAwareness(1)
except ImportError:
    print("Error: windll not imported. Text may be blurred")
    pass

from gui.components.get_media import GetMediaBtn, MediaList
from gui.components.text_field import TextField

class EditPosts(tk.Frame):
    def __init__(self, container, main_window):
        super().__init__(container)

        #GROUPER FRAMES
        self.main_frame = tk.Frame(self, bg="purple")
        self.main_frame.pack(fill='both')
        self.header_frame = tk.Frame(self.main_frame)
        self.header_frame.pack(fill='x',padx=10, pady=10)
