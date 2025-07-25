import tkinter as tk

from app.gui.styles import BaseStyle
from app.util.image_tools import load_icon

class OpenButton(tk.Button):
    def __init__(self, master, command, height = 20, text=None, **kwargs):
        self.command = command
        self.style = BaseStyle()
        self.icon = load_icon("open_icon.png", height)
        super().__init__(master,
                         image=self.icon,
                         compound="left" if self.icon else None,
                         command=self.command,
                         background=self.style.background,
                         activebackground=self.style.pressed,
                         **kwargs)
        if text:
            self.config(text=text, foreground=self.style.foreground)
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)
    
    def on_enter(self, e):
        self.config(bg=self.style.activebackground)

    def on_leave(self,e):
        self.config(bg=self.style.background)

