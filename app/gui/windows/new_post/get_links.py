import tkinter as tk
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo
import os
from PIL import Image, ImageTk


from app.gui.styles import BaseStyle
from app.gui.widgets.buttons import Button
from app.gui.widgets.text import Text, Entry
from app.gui.widgets.frames import WidgetFrame
from app.gui.widgets.labels import WidgetLabel

from app.gui.windows.new_post.build_post import BuildPostButton

from app.util.controller import JsonController
from app.util.extensions import Extensions
from app.util.models.link import LinkObj, LinkCollection, LinkEntryFrame
from app.util.controllers.post_controller import PostController

class LinkEntriesFrame(tk.Frame):
    def __init__(self, container:tk.Frame, link_collection: LinkCollection):
        super().__init__(container)
        self.style = BaseStyle()
        self.config(background=self.style.widget_background)
        self.link_collection = link_collection
        
    def update(self):
        if len(self.link_collection.entries) == 0:
            return
        for link_obj in self.link_collection.entries:
            if not isinstance(link_obj, LinkObj):
                self.link_collection.entries.remove(link_obj)
                continue
            if link_obj and link_obj.delete:
                self.link_collection.entries.remove(link_obj)
                continue
            if not link_obj.link_entry_frame:
                new_link_entry_frame = LinkEntryFrame(self, link_obj)
                new_link_entry_frame.pack()

class AddLinkBtn(tk.Frame):
    def __init__(self, container:tk.Frame, link_collection: LinkCollection, link_entries_frame: LinkEntriesFrame):
        super().__init__(container)
        btn = Button(self, command=self.add_new_link_entry, text="Add Link", width=20)
        btn.pack(fill="x", expand=True)
        self.link_collection = link_collection
        self.link_entries_frame = link_entries_frame    

    def add_new_link_entry(self):
        new_link = LinkObj()
        self.link_collection.entries.append(new_link)
        self.link_entries_frame.update()