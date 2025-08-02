import tkinter as tk
from tkinter import filedialog
from app.gui.styles import BaseStyle
from app.util.image_tools import load_icon

class Button(tk.Button):
    def __init__(self, master, command, text, fontsize=12, width = None):
        self.style = BaseStyle()
        super().__init__(master, 
                         command=command, 
                         text=text,
                         background=self.style.background,
                         activebackground=self.style.pressed,
                         font=(self.style.font_family, fontsize),
                        foreground= self.style.foreground)
        if width:
            self.config(width=width)
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)

    def on_enter(self, e):
        self.config(bg=self.style.activebackground)

    def on_leave(self,e):
        self.config(bg=self.style.background)
        
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

class FileUploader(tk.Frame):
    def __init__(self, parent, callback=None, button_text="Upload File", filetypes = [("All Files", "*.*")],**kwargs):
        super().__init__(parent, **kwargs)
        self.filetypes = filetypes
        self.callback = callback
        self.file_path = None

        self.upload_button = Button(self, text=button_text, command=self.open_file_dialog)
        self.upload_button.pack(padx=10, pady=10)

    def open_file_dialog(self):
        filetypes = self.filetypes
        selected_file = filedialog.askopenfilename(title="Select a file", filetypes=filetypes)
        if selected_file:
            self.file_path = selected_file
            if self.callback:
                self.callback(selected_file)

    def get_selected_file(self):
        return self.file_path
