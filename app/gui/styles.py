from tkinter import ttk

class BaseStyle:
    def __init__(self, font_size:int = 14, widget_width:int = None):
        style = ttk.Style()
        self.style_name = "Custom.TMenubutton"

        self.foreground = "white"
        self.background = "black"
        self.font = ("Helvetica", font_size)
        self.activebackground = '#333333'
        self.activeforeground = "white"
        self.pressed = '#CAA71C'


        if widget_width:
            style.configure(self.style_name, width=widget_width)

        style.configure(self.style_name,
                        foreground=self.foreground,  
                        background=self.background,  
                        font=self.font)  
        style.map(self.style_name,
                  background=[('active', self.activebackground), ('!disabled', 'black')],
                  foreground=[('!disabled', self.activeforeground)])
    
    