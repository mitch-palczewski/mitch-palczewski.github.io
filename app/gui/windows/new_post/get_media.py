import tkinter as tk
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo, askyesno
import os
from PIL import Image, ImageTk


from app.gui.styles import BaseStyle
from app.gui.widgets.buttons import Button
from app.gui.widgets.text import Text
from app.gui.widgets.frames import WidgetFrame
from app.gui.widgets.labels import WidgetLabel, InfoIcon

from app.gui.windows.new_post.build_post import BuildPostButton

from app.util.controller import JsonController
from app.util.extensions import Extensions, VALID_HTML_IMAGE_EXTENSIONS, VALID_HTML_VIDEO_EXTENSIONS
from app.util.models.media import MediaObj, MediaCollection
from app.util.controllers.post_controller import PostController

MAX_IMG_HEIGHT = 600
MAX_IMG_WIDTH = 700

class ImageEntryFrame(WidgetFrame):
    def __init__(self, container:tk.Frame, media:MediaObj):
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
    def __init__(self, container:tk.Frame, media:MediaObj):
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
    def __init__(self, container:tk.Frame, media:MediaObj):
        super().__init__(container)
        self.style = BaseStyle()
        self.media = media
        self.columnconfigure(0, weight=4)
        self.columnconfigure(1, weight=1)
        self.pack(fill='x', expand=True, pady=5)
        text_entry = Text(self)
        media.text_obj = text_entry
        text_entry.grid(column=0,row=0)
        text = self.media.text
        if text:
            text_entry.insert_begining(text)
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
    def __init__(self, container:tk.Frame, media_collection:MediaCollection, post_controller: PostController):
        super().__init__(container)
        self.style = BaseStyle()
        self.config(background=self.style.widget_background)
        self.entries = media_collection.entries
        self.tk_entries = media_collection.tk_entries
        self.media_content = tk.Frame(self, bg=self.style.widget_background, width=MAX_IMG_WIDTH+20)
        self.media_content.pack(fill='both',padx=10, pady=10)
        self.build_btn = BuildPostButton(self, post_controller)
        self.build_btn_packed = False

    def update(self):
        self.get_text_from_text_entrys()
        self.media_content.destroy()
        self.media_content = tk.Frame(self, bg=self.style.widget_background, width=MAX_IMG_WIDTH+20)
        self.media_content.pack(fill='both', padx=10, pady=10)
        for entry in self.entries:
            if isinstance(entry, MediaObj):
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
            self.build_btn.pack(side='bottom', fill='x', expand=True)
    
    def forget_build_post_btn(self):
        self.build_btn.pack_forget()

    def get_text_from_text_entrys(self):
        for entry in self.entries:
            if not isinstance(entry, MediaObj):
                continue
            if entry.entry_type == 'text' and entry.text_obj:
                entry.text = entry.text_obj.get_all()





class UploadMediaBtn(tk.Frame):
    def __init__(self, container:tk.Frame, media_collection:MediaCollection, media_entries_frame: MediaEntriesFrame, entry_type:str, accepted_filetypes:tuple = None):
        super().__init__(container)
        self.entries:list = media_collection.entries
        self.tk_entries:list = media_collection.tk_entries
        self.accepted_filetypes:tuple = accepted_filetypes
        self.media_entries_frame: MediaEntriesFrame = media_entries_frame
        self.max_entries = media_collection.max_entries
        self.frame = WidgetFrame(self)
        self.frame.pack(fill="x", expand=True)
        info_icon = None
        btn = Button(self.frame, command=self.add_new_media_entry, text="Upload", width=20)
        if entry_type == "image":
            btn.config(text="Upload Image",
                       command=self.add_new_media_entry)
            info_icon = InfoIcon(self.frame, f"Upload a image with extension: \n {VALID_HTML_IMAGE_EXTENSIONS}")
        elif entry_type == "video":
            btn.config(text="Upload Video",
                       command=self.add_new_media_entry)
            info_icon = InfoIcon(self.frame, f"Perfered Video extension is mp4 but accepted are: \n {VALID_HTML_VIDEO_EXTENSIONS}")
        elif entry_type == "text":
            btn.config(text="Add Text",
                       command=self.make_text_obj)
        btn.pack(fill="x", expand=True, side='left')
        if info_icon:
            info_icon.pack(side='left',padx=3)
    
    def add_new_media_entry(self):
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
        new_entry = MediaObj()
        if Extensions.is_valid_html_image(file_path):
            new_entry.entry_type = 'image' 
            new_entry.file_path = file_path
            new_entry.tk_photoimage = path_to_tk_image(file_path)
            self.entries.append(new_entry)
            self.media_entries_frame.update()
        if Extensions.is_valid_html_video(file_path):
            file_mb = os.path.getsize(file_path)/ (1024 * 1024)
            if file_mb > 10 :
                answer = askyesno(
                    "Video over 10mb", 
                    "The video you selected is greater then 10mb. " \
                    "\n Github does not allow videos of size greater then 10mb" \
                    "\n Would you like to continue")
                if not answer:
                    return
            new_entry.entry_type = 'video'
            new_entry.file_path = file_path
            self.entries.append(new_entry)
            self.media_entries_frame.update()
        self.media_entries_frame.pack_build_post_btn()
    
    def make_text_obj(self):
        new_entry = MediaObj()
        new_entry.entry_type = "text"
        self.entries.append(new_entry)
        self.media_entries_frame.update()
    

def entries_maxed(entries, max_entries):
    count = 0 
    for entry in entries:
        if isinstance(entry, MediaObj):
            if not entry.delete:
                count += 1
        else:
            ValueError(entry, "Entry is not instance of Media")
    if max_entries and count >= max_entries:
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




        