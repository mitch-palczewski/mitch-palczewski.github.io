from tkinter import ttk
import tkinter as tk

from app.gui.styles import BaseStyle

class OptionMenu(ttk.OptionMenu):
    def __init__(self, master, initial_option, options, command, widget_width=10):
        self._selected_value = tk.StringVar()
        self.options = options
        om_style = BaseStyle(widget_width=widget_width, font_size=20)
        super().__init__(
            master,
            self._selected_value,
            initial_option,
            *self.options,
            command=command,
            style= om_style.style_name
        )

        self.menu:tk.Menu = self["menu"]
        self.menu.config(
            background = om_style.background,
            foreground = om_style.foreground,
            font = (om_style.font[0], 18),
            borderwidth=3,
            activebackground=om_style.pressed
        )
        
    @property
    def selected_value(self):
        return self._selected_value.get()
    
    @selected_value.setter
    def selected_value(self, value):
        if not value in self.options:
            ValueError(f"{value} is not in {self.options}")
        self._selected_value.set(value)
    
    
