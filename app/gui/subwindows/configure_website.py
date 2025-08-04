import tkinter as tk
from tkinter import font
try:
    from ctypes import windll
    windll.shcore.SetProcessDpiAwareness(1)
except ImportError:
    print("Error: windll not imported. Text may be blurred")
    pass

from app.gui.subwindows.configure_windows.general_config import GeneralConfig
from app.util.controller import JsonController
colors = JsonController.get_config_data("colors")
C1 = colors["c1"]
C2 = colors["c2"]
C3 = colors["c3"]
C4 = colors["c4"]
C5 = colors["c5"]


class ConfigureWebsite(tk.Frame):
    def __init__(self, container, main_window):
        super().__init__(container)
        FONT_SM = font.Font(family="Helvetica", size=10)

        #GROUPER FRAMES
        main_frame = tk.Frame(self, bg=C1)
        main_frame.pack(fill='both')

        #HEADER
        header_frame = tk.Frame(main_frame, bg=C1)
        header_frame.columnconfigure(0, weight=1)
        header_frame.columnconfigure(1, weight=1)
        header_frame.columnconfigure(2, weight=1)
        header_frame.columnconfigure(3, weight=1)

        header_frame.pack(fill="x", expand=True)
        btn_padx = 10
        btn_pady = 10
        self.general_config_btn = tk.Button(
            header_frame, 
            text="General Configuration", 
            command=lambda:self.load_content("GeneralConfig"),
            bg="white",
            font=FONT_SM
        )
        self.general_config_btn.grid(column=0, row=0, sticky=tk.EW, padx=btn_padx, pady=btn_pady)
        
        

        
        #BODY
        self.body_frame = tk.Frame(self, bg=C1)
        self.body_frame.pack(fill='both', expand= True)
        self.body_content = None


        self.load_content("GeneralConfig")

    def set_btns_color(self, color):
        self.general_config_btn.config(bg=color)
        
    def new_content_frame(self):
        if self.body_content:
            self.body_content.destroy()
        self.body_content = tk.Frame(self.body_frame, bg=C1)
        self.body_content.pack(fill='both', expand= True)

    def load_content(self, content:str):
        """
        Accepts content: "GeneralConfig", 
        """
        self.set_btns_color(C5)
        self.new_content_frame()

        if content == "GeneralConfig":
            general_config = GeneralConfig(self.body_content)
            general_config.pack(fill='both', expand= True)
            self.general_config_btn.config(bg=C4)
            return
        print(f"{content} is not set up")
        