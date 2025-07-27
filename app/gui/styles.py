from tkinter import ttk

class BaseStyle:
    def __init__(self, font_size:int = 14, widget_width:int = None):
        style = ttk.Style()
        self.style_name = "Custom.TMenubutton"


        self.foreground = "white"
        self.background = "black"
        self.font_size = font_size
        self.font_family = "Helvetica"
        self.font = (self.font_family, self.font_size)
        self.activebackground = '#333333'
        self.activeforeground = "white"
        self.pressed = '#CAA71C'
        self.page_background = '#E0E5E9'
        self.widget_background = '#F1EFE8'


        if widget_width:
            style.configure(self.style_name, width=widget_width)

        style.configure(self.style_name,
                        foreground=self.foreground,  
                        background=self.background,  
                        font=self.font)  
        style.map(self.style_name,
                  background=[('active', self.activebackground), ('!disabled', 'black')],
                  foreground=[('!disabled', self.activeforeground)])
    
