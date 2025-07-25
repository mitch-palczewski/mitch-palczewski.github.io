import tkinter as tk
from app.util.image_tools import load_icon  
from app.gui.styles import BaseStyle
from screeninfo import get_monitors


class Label(tk.Label):
    def __init__(self, master, text, font_size = 12, **kwargs):
        self.style = BaseStyle(font_size=font_size)
        super().__init__(
            master, 
            text=text,  
            justify="left",
            font=self.style.font,
            **kwargs)


class InfoIcon(tk.Label):
    def __init__(self, master, text, icon_height=30, **kwargs):
        super().__init__(master, **kwargs)
        self.style = BaseStyle()
        self.icon = load_icon("info_icon.png", icon_height)
        self.config(image=self.icon, cursor="hand2", background=self.style.background, height=icon_height)

        self.tooltip_win = tk.Toplevel(master)
        self.tooltip_win.wm_overrideredirect(True)  
        self.tooltip_win.attributes("-topmost", True)  
        self.tooltip_win.withdraw()  

        self.tooltip_label = tk.Label(
            self.tooltip_win,
            text=text,
            justify="left",
            bg=self.style.background,
            fg=self.style.foreground,
            font=(self.style.font[0], 12),
            relief="solid",
            bd=1
        )
        self.tooltip_label.pack(ipadx=3, ipady=3)

        self.bind("<Enter>", self.show_tooltip)
        self.bind("<Leave>", self.hide_tooltip)

    def show_tooltip(self, event):
        self.tooltip_win.update_idletasks()

        # actual tooltip dimensions
        tw = self.tooltip_win.winfo_width()
        th = self.tooltip_win.winfo_height()

        # mouse location (screen coords)
        mx, my = event.x_root, event.y_root

        # find the monitor under the mouse
        for m in get_monitors():
            if m.x <= mx <= m.x + m.width and m.y <= my <= m.y + m.height:
                sx, sy, sw, sh = m.x, m.y, m.width, m.height
                break
        else:
            # fallback to primary screen
            sx, sy = 0, 0
            sw = self.winfo_screenwidth()
            sh = self.winfo_screenheight()

        # default: right + above
        x = self.winfo_rootx() + 5
        y = self.winfo_rooty() - th - 5

        # clamp horizontally
        if x + tw > sx + sw:
            x = sx + sw - tw - 5
        if x < sx:
            x = sx + 5

        # clamp vertically (flip below if needed)
        if y < sy:
            y = self.winfo_rooty() + self.winfo_height() + 5
        if y + th > sy + sh:
            y = sy + sh - th - 5

        self.tooltip_win.geometry(f"+{x}+{y}")
        self.tooltip_win.deiconify()



    def hide_tooltip(self, event):
        self.tooltip_win.withdraw()  

