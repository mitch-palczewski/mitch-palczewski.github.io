import tkinter as tk
from tkinter import ttk, font
from bs4 import BeautifulSoup as bs

try:
    from ctypes import windll
    windll.shcore.SetProcessDpiAwareness(1)
except ImportError:
    print("Error: windll not imported. Text may be blurred")
    pass


from app.gui.components.text_field import TextField



from app.util.controllers.post_controller import PostController

from app.gui.widgets.scrollable_frame import ScrollableFrame
from app.gui.widgets.options_menu import OptionMenu
from app.gui.widgets.buttons import OpenButton
from app.gui.widgets.labels import InfoIcon, InfoIconLight,WidgetLabel
from app.gui.widgets.text import Entry, ScrollText
from app.gui.widgets.frames import  BorderWidgetFrame, WidgetFrame
from app.gui.styles import BaseStyle

from app.gui.windows.new_post.build_post import BuildPostButton
from app.gui.windows.new_post.get_media import UploadMediaBtn, MediaEntriesFrame, MediaCollection
from app.gui.windows.new_post.get_links import AddLinkBtn, LinkCollection, LinkEntriesFrame


from app.util.extensions import Extensions
from app.util.controller import JsonController, FileController, Controller

MAX_MEDIA_ITEMS = 1
CAPTION_FEILD_HEIGHT = 25
colors = JsonController.get_config_data("colors")
C1 = colors["c1"]
C2 = colors["c2"]
C3 = colors["c3"]
C4 = colors["c4"]

INFO_ICON_SIZE = 36
OPEN_BUTTON_SIZE = INFO_ICON_SIZE - 2
TEXT_ENTRY_WIDTH = 100
TEXT_FONT_SIZE = 16

class NewPostFrame(tk.Frame):
    def __init__(self, container, main_window):
        super().__init__(container)
        post_controller = PostController()
        post_controller.main_window = main_window
        scroll_frame = ScrollableFrame(self)
        scroll_frame.pack(fill="both", expand=True)
        scrollable_frame = scroll_frame.get_scrollable_frame()
        form_frame = FormFrame(scrollable_frame, post_controller)
        form_frame.pack( pady=10, padx=10)
        
class FormFrame(tk.Frame):
    def __init__(self, container, post_controller:PostController):
        super().__init__(container)
        style = BaseStyle()
        self.config(background=style.page_background)
        upload_media_frame = UploadMediaFrame(self, post_controller)
        header_frame = tk.Frame(self,
                                highlightbackground=style.background,
                                highlightcolor=style.background,
                                highlightthickness=5,
                                background=style.widget_background)
        header_frame.columnconfigure(0, weight=1)
        header_frame.columnconfigure(1, weight=1)
        header_frame.pack(fill='x', pady=10)
        post_type_frame = PostTypeFrame(header_frame, upload_media_frame)
        post_type_frame.grid(row=0, column=0, padx=10, pady=10)
        post_theme_frame = PostThemeFrame(header_frame, post_controller)
        post_theme_frame.grid(row=0, column=1, padx=10, pady=10)

        body_frame = tk.Frame(self, background=style.widget_background)
        body_frame.pack(pady=10)
        post_title_frame = PostTitleFrame(body_frame, post_controller)
        post_title_frame.pack(fill='x', padx=10,pady=10)
        post_caption_frame = PostCaptionFrame(body_frame, post_controller)
        post_caption_frame.pack(fill="x", padx=10,pady=10)

        add_links_frame = AddLinksFrame(self, post_controller)
        add_links_frame.pack(fill="x", expand=True,  pady=10)

        upload_media_frame.pack(fill='x', expand=True,  pady=10)

class AddLinksFrame(BorderWidgetFrame):
    def __init__(self, container, post_controller:PostController):
        super().__init__(container)
        link_collection = LinkCollection()
        post_controller.link_collection = link_collection
        link_entries_frame = LinkEntriesFrame(self, link_collection)
        add_link_btn = AddLinkBtn(self,link_collection, link_entries_frame)
        add_link_btn.pack(pady=3)
        link_entries_frame.pack()

class UploadMediaFrame(BorderWidgetFrame):
    def __init__(self, container, post_controller:PostController):
        super().__init__(container)
        self.upload_frame:tk.Frame = WidgetFrame(self)
        temp_lbl = WidgetLabel(self.upload_frame, "Select a post type to upload media.")
        temp_lbl.pack(padx=3, pady=3)
        self.upload_frame.pack()
        self.post_controller = post_controller
        
    def set_post_type(self, post_type):
        if self.upload_frame:
            self.upload_frame.forget()
        if post_type == "Select Post Type":
            self.upload_frame.pack_forget()
        if post_type == "Text Post":
            self.upload_frame = WidgetFrame(self)
            self.upload_frame.pack()
            self.build_btn = BuildPostButton(self.upload_frame, self.post_controller)
            self.build_btn.pack(fill='x')
            self.post_controller.post_type = 'text'
        if post_type == "Image Post":
            self.upload_frame = ImageUploadFrame(self, self.post_controller)
            self.post_controller.post_type = 'image'
            self.upload_frame.pack(fill='x')
        if post_type == "Video Post":
            self.upload_frame = VideoUploadFrame(self, self.post_controller)
            self.post_controller.post_type = 'video'
            self.upload_frame.pack(fill='x')
        if post_type == "Gallery Post":
            self.upload_frame = GalleryUploadFrame(self, self.post_controller)
            self.post_controller.post_type = 'gallery'
            self.upload_frame.pack(fill='x')
        self.pack()
     
class PostTypeFrame(tk.Frame):
    def __init__(self, container, upload_type_frame: UploadMediaFrame):
        super().__init__(container)
        style = BaseStyle()
        self.upload_type_frame = upload_type_frame
        self.config(background=style.widget_background)
        type_info = (
        "The Post Type Determines what type of media is present in your post.\n" \
        "Use the Gallery Post to include multiple Images, Videos, or blocks of text")
        selectable_types = ["Select Post Type", "Text Post", "Image Post", "Video Post", "Gallery Post"]
        label = WidgetLabel(self, text="Post Type:", font_size = TEXT_FONT_SIZE)
        label.pack(fill=tk.X, padx=5, pady=5, side="left")
        self.option_menu = OptionMenu(
            self,
            selectable_types[0],
            selectable_types,
            self.on_select,
            15
        )
        self.option_menu.pack(side="left")
        info = InfoIcon(self, type_info, INFO_ICON_SIZE)
        info.pack(side="left", padx=3)
        
    def on_select(self, selected_value):
        self.upload_type_frame.set_post_type(selected_value)


class PostThemeFrame(tk.Frame):
    def __init__(self, container, post_controller:PostController):
        super().__init__(container)
        style = BaseStyle()
        self.config(background=style.widget_background)
        self.post_controller = post_controller
        type_info = (
            "Select a Theme for your post. Themes html files can be modified for personal customization.\n"
            "Select the open button to view the selected theme")
        selectable_types = ["base.html"]
        print("TODO get list of available themes")
        label = WidgetLabel(self, text="Post Theme:", font_size = TEXT_FONT_SIZE)
        label.pack(fill=tk.X, padx=5, pady=5, side="left")
        option_menu = OptionMenu(
            self,
            selectable_types[0],
            selectable_types,
            self.on_select,
            15
        )
        option_menu.pack(side="left")
        test = OpenButton(self , self.open_theme, height=OPEN_BUTTON_SIZE)
        test.pack(side="left", padx=3)
        info = InfoIcon(self, type_info, INFO_ICON_SIZE)
        info.pack(side="left")
        
            
    def on_select(self):
        
        pass

    def open_theme(self):
        pass

class PostTitleFrame(tk.Frame):
    def __init__(self, container, post_controller: PostController):
        super().__init__(container)
        header = tk.Frame(self)
        header.pack(fill='x')
        label = WidgetLabel(header, "Post Title:", TEXT_FONT_SIZE)
        label.pack(side='left')
        info_icon = InfoIconLight(header, "Enter Post Title. Title is limited to a single line.", INFO_ICON_SIZE)
        info_icon.pack(side='left', padx=3)
        title_entry = Entry(self, width = 75, font_size=14)
        title_entry.pack(side='left')
        post_controller.title_entry = title_entry

class PostCaptionFrame(tk.Frame):
    def __init__(self, container, post_controller: PostController):
        super().__init__(container)
        header = tk.Frame(self)
        header.pack(fill='x')
        label = WidgetLabel(header, "Post Caption:", TEXT_FONT_SIZE)
        label.pack(side='left')
        info_icon = InfoIconLight(header, "Enter Post Caption. Can include multiple paragraphs", INFO_ICON_SIZE)
        info_icon.pack(side='left', padx=3)
        caption_entry = ScrollText(self, width=75, height=12, font_size=14)
        caption_entry.pack(side='left')
        post_controller.caption_entry = caption_entry


class ImageUploadFrame(tk.Frame):
     def __init__(self, container, post_controller: PostController):
        super().__init__(container)
        filetypes = Extensions.get_tkinter_filetypes(True, False)
        media_collection = MediaCollection(max_items=1)
        post_controller.media_collection = media_collection
        media_entries_frame= MediaEntriesFrame(
            self, 
            media_collection,
            post_controller)
        upload_media_btn = UploadMediaBtn(
            self, 
            media_collection, 
            media_entries_frame,
            accepted_filetypes=filetypes,
            entry_type="image")
        upload_media_btn.pack(padx=10, pady=10, fill="x")
        media_entries_frame.pack()

class VideoUploadFrame(tk.Frame):
    def __init__(self, container, post_controller: PostController):
        super().__init__(container)
        filetypes = Extensions.get_tkinter_filetypes(False, True)
        media_collection = MediaCollection(max_items=1)
        post_controller.media_collection = media_collection
        media_entries_frame= MediaEntriesFrame(
            self, 
            media_collection,
            post_controller)
        upload_media_btn = UploadMediaBtn(
            self, 
            media_collection, 
            media_entries_frame,
            accepted_filetypes=filetypes,
            entry_type="video")
        upload_media_btn.pack(padx=10, pady=10, fill="x")
        media_entries_frame.pack()

class GalleryUploadFrame(tk.Frame):
    def __init__(self, container, post_controller: PostController):
        super().__init__(container)
        image_filetypes = Extensions.get_tkinter_filetypes(True, False)
        video_filetypes = Extensions.get_tkinter_filetypes(False, True)
        btn_frame = WidgetFrame(self)
        btn_frame.pack()
        media_collection = MediaCollection()
        post_controller.media_collection = media_collection
        media_entries_frame= MediaEntriesFrame(
            self, 
            media_collection,
            post_controller)
        upload_image_btn = UploadMediaBtn(
            btn_frame, 
            media_collection, 
            media_entries_frame,
            accepted_filetypes= image_filetypes,
            entry_type="image")
        upload_image_btn.pack(padx=10, pady=10, fill="x",expand=True, side='left')
        upload_video_btn = UploadMediaBtn(
            btn_frame, 
            media_collection, 
            media_entries_frame,
            accepted_filetypes=video_filetypes,
            entry_type="video")
        upload_video_btn.pack(padx=10, pady=10, fill="x",expand=True, side="left")
        upload_text_btn= UploadMediaBtn(
            btn_frame, 
            media_collection, 
            media_entries_frame,
            entry_type="text")
        upload_text_btn.pack(padx=10, pady=10, fill="x", expand=True, side='left')
        media_entries_frame.pack(fill='x', expand=True)


