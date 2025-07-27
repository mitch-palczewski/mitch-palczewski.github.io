from tkinter.scrolledtext import ScrolledText
import tkinter as tk

from app.gui.styles import BaseStyle

class ScrollText(ScrolledText):
    def __init__(self, master, width:int = 80, height:int = 10, font_size = 12, **kwargs):
        style = BaseStyle()
        super().__init__(
            master, 
            width = width, 
            height=height,
            highlightthickness=3,
            highlightbackground=style.background,
            highlightcolor= style.background,
            bg= style.activebackground,
            fg=style.foreground,
            insertbackground = style.foreground,
            font = (style.font[0], font_size),
            **kwargs
        )

    def get_all(self):
        return self.get("1.0", "end-1c")
    

class Entry(tk.Entry):
    def __init__(self,
                 master,
                 width: int = 20,
                 font_size = 12,
                 **kwargs):
        style = BaseStyle()

        super().__init__(
            master,
            width=width,
            highlightthickness=3,
            highlightbackground=style.background,
            highlightcolor=style.background,
            bg=style.activebackground,
            fg=style.foreground,
            insertbackground=style.foreground,
            font=(style.font[0], font_size),
            **kwargs
        )





