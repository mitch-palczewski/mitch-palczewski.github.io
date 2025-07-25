import tkinter as tk
from tkinter import ttk

class RadioHeader(ttk.LabelFrame):
    def __init__(self, master, title, options, command=None, **kwargs):
        super().__init__(master, text=title, **kwargs)
        self.selected = tk.StringVar(value=options[0])
        self.radio_frame = ttk.Frame(self)
        self.radio_frame.pack(padx=10, anchor="n")
        for option in options:
            rb = ttk.Radiobutton(
                self.radio_frame,
                text=option,
                variable=self.selected,
                value=option,
                command=lambda opt=option: command(opt) if command else None
            )
            rb.pack(side="left", padx=5)
        self.pack(padx=10, pady=(0,10), fill="x")

if __name__ == "__main__":
    def on_select(value):
        print(f"Selected: {value}")

    root = tk.Tk()
    root.title("RadioHeader Demo")

    header = RadioHeader(
        master=root,
        title="Settings Panel",
        options=["Basic", "Advanced", "Expert"],
        command=on_select
    )
    ttk.Label(header, text="Adjust your preferences here.").pack(padx=10, pady=10)

    root.mainloop()