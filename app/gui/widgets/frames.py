import tkinter as tk 
from app.gui.styles import BaseStyle


class WidgetFrame(tk.Frame):
    def __init__(self, container, has_border):
        self.has_border = has_border
        style = BaseStyle()
        super().__init__(container, 
            background=style.widget_background)
        if has_border == True:
            self.config(highlightbackground=style.background,
            highlightcolor=style.background,
            highlightthickness=5)

class BorderWidgetFrame(tk.Frame):
    def __init__(self, container):
        style = BaseStyle()
        super().__init__(container, 
            background=style.widget_background,
            highlightbackground=style.background,
            highlightcolor=style.background,
            highlightthickness=5)

class WidgetFrame(tk.Frame):
    def __init__(self, container):
        style = BaseStyle()
        super().__init__(container,
            background=style.widget_background,
           )