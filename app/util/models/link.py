from dataclasses import dataclass
import tkinter as tk
from app.gui.widgets.text import Entry
from app.gui.widgets.frames import WidgetFrame
from app.gui.widgets.buttons import Button
from app.gui.styles import BaseStyle



@dataclass
class LinkObj:
    _link:str = None
    _link_text:str = None
    link_entry:Entry = None
    link_text_entry:Entry = None
    link_entry_frame:"LinkEntryFrame" = None
    delete: bool = False

    @property
    def link(self):
        self._link = self.link_entry.get()
        return self._link
    @link.setter
    def link(self, value:str):
        self._link = value

    @property
    def link_text(self):
        self._link_text = self.link_text_entry.get()
        return self._link_text
    @link_text.setter
    def link_text(self, value:str):
        self._link_text = value


class LinkCollection:
    def __init__(self):
        self._entries = []
    
    @property
    def entries(self):
        for entry in self._entries:
            if not LinkCollection.validate_entry(entry):
                self._entries.remove(entry)
        return self._entries
    @entries.setter
    def entries(self, value:list):
        for entry in value:
            if not LinkCollection.validate_entry(entry):
                value.remove(entry)
        self._entries = value
    
    def get_all_links(self):
        links = []
        for link_obj in self.entries:
            if not isinstance(link_obj, LinkObj):
                self.entries.remove(link_obj)
                continue
            link = link_obj.link
            if not link:
                self.entries.remove(link_obj)
                continue
            link_text = link_obj.link_text
            if not link_text:
                link_text = link
            links.append((link, link_text))
        return links
            

    @staticmethod
    def validate_entry(entry):
        if not isinstance(entry, LinkObj):
            return False
        if entry.delete:
            return False
        return True
    
class LinkEntryFrame(WidgetFrame):
    def __init__(self, container:tk.Frame, link:LinkObj):
        super().__init__(container)
        self.config(highlightbackground='black', highlightcolor='black', highlightthickness=1)
        self.link = link
        self.link.link_entry_frame = self
        self.style = BaseStyle()
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=4)
        self.columnconfigure(2, weight=1)
        self.pack(fill='x', expand=True, pady=5)
        lbl1 = tk.Label(self, text="Link:", font=self.style.font)
        lbl1.grid(column=0, row=0, sticky=tk.E)
        lbl2 = tk.Label(self, text="Link Text:", font=self.style.font)
        lbl2.grid(column=0, row=1, sticky=tk.E)
        link_entry = Entry(self, 60)
        link_entry.grid(column=1, row=0)
        self.link.link_entry = link_entry
        link_text_entry = Entry(self, 60)
        link_text_entry.grid(column=1, row=1, pady=(0,3))
        self.link.link_text_entry = link_text_entry
        x_btn = Button(
            self, 
            text="x", 
            command= self.set_delete,
        )
        x_btn.grid(column=2, row=0, sticky=tk.E, padx=3, pady=3, columnspan=2)

    def set_delete(self):
        self.link.delete = True
        self.pack_forget()


