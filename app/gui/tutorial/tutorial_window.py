import tkinter as tk

from app.gui.components.scroll_frame import ScrollFrame
from app.util.controller import JsonController

class TutorialWindow:
    def __init__(self, root):
        self.prev_content = None 
        self.content = None

        self.tutorial_root = tk.Toplevel(root)
        self.tutorial_root.title("Tutorial")
        self.tutorial_root.geometry("200x400")
        scroll_frame = ScrollFrame(self.tutorial_root)
        scroll_frame.pack(fill="both", expand=True)
        scroll_frame_body = scroll_frame.inner_frame
        self.body = tk.Frame(scroll_frame_body)
        self.body.pack()
        lbl = tk.Label(self.body, text="hello")
        lbl.pack()

        self.content = Welcome(self.body, self)
        self.content.pack()
        self.prev_content = self.content
    
    def load_content(self, new_content: tk.Widget):
        self.prev_content= self.content
        self.content.pack_forget()
        self.content = new_content
        self.content.pack()

class Welcome(tk.Frame):
    def __init__(self, container: tk.Frame, master:TutorialWindow):
        super().__init__(container)

        hosting_choices = tk.Frame(container )
        hosting_choices.columnconfigure(1, weight=1)
        hosting_choices.columnconfigure(2, weight=1)
        hosting_choices.columnconfigure(3, weight=1)
        hosting_choices.pack()

        github_btn = tk.Button(hosting_choices, text= "Github", command=lambda: master.load_content(GithubConfig(container)))
        github_btn.grid(row=0, column=0)
        pass

class GithubConfig(tk.Frame):
    def __init__(self, container):
        super().__init__(container)
        pass

class NeocitiesConfig(tk.Frame):
    def __init__(self, container):
        super().__init__(container)
        pass

class OtherConfig(tk.Frame):
    def __init__(self, container):
        super().__init__(container)
        pass

class PageConfig(tk.Frame):
    def __init__(self, container):
        super().__init__(container)
        pass

class FirstPost(tk.Frame):
    def __init__(self, container):
        super().__init__(container)
        pass

def init_tutorial(root):
    first_load:bool = JsonController.get_config_data("first_load")
    if first_load:
        return TutorialWindow(root)