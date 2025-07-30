import tkinter as tk
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo
import os
from PIL import Image, ImageTk
from dataclasses import dataclass



from app.gui.styles import BaseStyle
from app.gui.widgets.buttons import Button
from app.gui.widgets.text import Text
from app.gui.widgets.frames import WidgetFrame
from app.gui.widgets.labels import WidgetLabel

from app.gui.windows.new_post.build_post import BuildPostButton

from app.util.controller import JsonController
from app.util.controllers.extensions import Extensions

MAX_IMG_HEIGHT = 600
MAX_IMG_WIDTH = 700

@dataclass
class Media:
    entry_type:str = None
    file_path:str = None
    tk_photoimage:str = None
    text:str = None
    text_obj:Text = None
    delete:bool = False

class MediaCollection:
    def __init__(self, max_items:int = None):
        self.max_entries = max_items
        self.entries = []
        self.tk_entries = []

class ImageEntryFrame(WidgetFrame):
    def __init__(self, container:tk.Frame, media:Media):
        super().__init__(container)
        self.style = BaseStyle()
        self.media = media
        self.container = container
        self.tk_image = self.media.tk_photoimage
        self.columnconfigure(0, weight=4)
        self.columnconfigure(1, weight=1)
        self.pack(fill='x', expand=True)
        lbl = tk.Label(self,  image=self.tk_image, font=self.style.font)
        lbl.grid(column=0, row=0)
        x_btn = Button(
            self, 
            text="x", 
            command= self.set_delete,
        )
        x_btn.grid(column=1, row=0, sticky=tk.E, padx=3)

    def set_delete(self):
        self.media.delete = True
        self.pack_forget()

class VideoEntryFrame(WidgetFrame):
    def __init__(self, container:tk.Frame, media:Media):
        super().__init__(container)
        self.style = BaseStyle()
        self.media = media
        self.container = container
        self.path = self.media.file_path
        self.columnconfigure(0, weight=4)
        self.columnconfigure(1, weight=1)
        self.pack(fill='x', expand=True)
        lbl = WidgetLabel(self, text="Video Post")
        lbl.grid(column=0, row=0)
        lbl_link = WidgetLabel(self, text=self.path)
        lbl_link.grid(column=0, row=1)
        x_btn = Button(
            self, 
            text="x", 
            command= self.set_delete,
        )
        x_btn.grid(column=1, row=0, sticky=tk.E, padx=3, rowspan=2)

    def set_delete(self):
        self.media.delete = True
        self.pack_forget()
        
class TextEntryFrame(WidgetFrame):
    def __init__(self, container:tk.Frame, media:Media):
        super().__init__(container)
        self.style = BaseStyle()
        self.media = media
        self.container = container
        
        self.columnconfigure(0, weight=4)
        self.columnconfigure(1, weight=1)
        self.pack(fill='x', expand=True)
        text_entry = Text(self)
        media.text_obj = text_entry
        text_entry.grid(column=0,row=0)
        x_btn = Button(
            self, 
            text="x", 
            command= self.set_delete,
        )
        x_btn.grid(column=1, row=0, sticky=tk.E, padx=3, rowspan=2)

    def set_delete(self):
        self.media.delete = True
        self.pack_forget()
        

class MediaEntriesFrame(tk.Frame):
    def __init__(self, container:tk.Frame, media_collection:MediaCollection):
        super().__init__(container)
        self.style = BaseStyle()
        self.config(background=self.style.widget_background)
        self.entries = media_collection.entries
        self.tk_entries = media_collection.tk_entries
        self.media_content = tk.Frame(self, bg=self.style.widget_background, width=MAX_IMG_WIDTH+20)
        self.media_content.pack(fill='both',padx=10, pady=10)
        self.build_btn = BuildPostButton(self)
        self.build_btn_packed = False

    def update(self):
        self.media_content.destroy()
        self.media_content = tk.Frame(self, bg=self.style.widget_background, width=MAX_IMG_WIDTH+20)
        self.media_content.pack(fill='both', padx=10, pady=10)
        for entry in self.entries:
            if isinstance(entry, Media):
                if entry.delete:
                    self.entries.remove(entry)
                    continue
                entry_type = entry.entry_type
                if entry_type == 'image':
                    new_entry_frame = ImageEntryFrame(self.media_content, entry)
                    new_entry_frame.pack()
                    continue
                if entry_type == 'video':
                    new_entry_frame = VideoEntryFrame(self.media_content, entry)
                    new_entry_frame.pack()
                    continue
                if entry_type == 'text':
                    new_entry_frame = TextEntryFrame(self.media_content, entry)
                    new_entry_frame.pack()
                    continue

    def pack_build_post_btn(self):
        if not self.build_btn_packed:
            self.build_btn.pack(side='bottom')
    
    def forget_build_post_btn(self):
        self.build_btn.pack_forget()
        
    def remove_media_element(self, index):
        del self.entries[index]
        del self.tk_entries[index]
        self.update()



class UploadMediaBtn(tk.Frame):
    def __init__(self, container:tk.Frame, media:MediaCollection, media_entries_frame: MediaEntriesFrame, entry_type:str, accepted_filetypes:tuple = None):
        super().__init__(container)
        self.entries:list = media.entries
        self.tk_entries:list = media.tk_entries
        self.accepted_filetypes:tuple = accepted_filetypes
        self.media_entries_frame: MediaEntriesFrame = media_entries_frame
        self.max_entries = media.max_entries
        btn = Button(self, command=self.get_media, text="Upload")
        if entry_type == "image":
            btn.config(text="Upload Image",
                       command=self.get_media)
        elif entry_type == "video":
            btn.config(text="Upload Video",
                       command=self.get_media)
        elif entry_type == "text":
            btn.config(text="Add Text",
                       command=self.make_text_obj)
        btn.pack(fill="x")
    
    def get_media(self):
        if entries_maxed(self.entries, self.max_entries):
            self.media_entries_frame.forget_build_post_btn()
            return
        file_path = fd.askopenfilename(
            title="media upload",
            initialdir=os.path.expanduser("~"),
            filetypes=self.accepted_filetypes
        )
        if not file_path:
            return
        new_entry = Media()
        if Extensions.is_valid_html_image(file_path):
            new_entry.entry_type = 'image' 
            new_entry.file_path = file_path
            new_entry.tk_photoimage = path_to_tk_image(file_path)
            self.entries.append(new_entry)
            self.media_entries_frame.update()
        if Extensions.is_valid_html_video(file_path): 
            new_entry.entry_type = 'video'
            new_entry.file_path = file_path
            self.entries.append(new_entry)
            self.media_entries_frame.update()
        self.media_entries_frame.pack_build_post_btn()
    
    def make_text_obj(self):
        new_entry = Media()
        new_entry.entry_type = "text"
        self.entries.append(new_entry)
        self.media_entries_frame.update()
    

def entries_maxed(entries, max_entries):
    count = 0 
    for entry in entries:
        if isinstance(entry, Media):
            if not entry.delete:
                count += 1
        else:
            ValueError(entry, "Entry is not instance of Media")
    if count >= max_entries:
        showinfo(title="Media Maxed",
                     message=f"Max of {max_entries} Entries")
        return True
    else: 
        return False


def path_to_tk_image(file_path) -> ImageTk.PhotoImage:
    img = Image.open(file_path)
    img.thumbnail((MAX_IMG_WIDTH, MAX_IMG_HEIGHT), Image.LANCZOS)
    photo = ImageTk.PhotoImage(img)
    return photo




        