import tkinter as tk
from tkinter import ttk, font
from bs4 import BeautifulSoup as bs

try:
    from ctypes import windll
    windll.shcore.SetProcessDpiAwareness(1)
except ImportError:
    print("Error: windll not imported. Text may be blurred")
    pass

from app.gui.components.get_media import GetMediaBtn, MediaList
from app.gui.components.text_field import TextField
from app.util.controller import JsonController, FileController, Controller

from app.gui.widgets.scrollable_frame import ScrollableFrame
from app.gui.widgets.options_menu import OptionMenu
from app.gui.widgets.buttons import OpenButton
from app.gui.widgets.labels import InfoIcon, InfoIconLight,Label
from app.gui.widgets.text import Entry, ScrollText
from app.gui.styles import BaseStyle

from app.util.models.post import Post
from app.util.models.theme import Theme
from app.util.models.webpage import Webpage
from app.util.view.post_to_html import PostHtmlRenderer

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
        scroll_frame = ScrollableFrame(self)
        scroll_frame.pack(fill="both", expand=True)
        scrollable_frame = scroll_frame.get_scrollable_frame()
        form_frame = FormFrame(scrollable_frame)
        form_frame.pack( pady=10, padx=10)
        

class UploadTypeFrame(tk.Frame):
    def __init__(self, container):
        super().__init__(container)
        style = BaseStyle()
        self.config(
            background=style.widget_background,
            highlightbackground=style.background,
            highlightcolor=style.background,
            highlightthickness=5)
        self.upload_frame:tk.Frame = None
        
    def set_post_type(self, post_type):
        if self.upload_frame:
            self.upload_frame.forget()
        if post_type == "Select Post Type":
            self.forget()
        if post_type == "Image Post":
            self.upload_frame = ImageUploadFrame(self)
            self.upload_frame.pack()
            self.pack()

class FormFrame(tk.Frame):
    def __init__(self, container):
        super().__init__(container)
        style = BaseStyle()
        self.config(background=style.page_background)
        upload_type_frame = UploadTypeFrame(self)
        header_frame = tk.Frame(self,
                                highlightbackground=style.background,
                                highlightcolor=style.background,
                                highlightthickness=5,
                                background=style.widget_background)
        header_frame.columnconfigure(0, weight=1)
        header_frame.columnconfigure(1, weight=1)
        header_frame.pack(fill='x', pady=10)
        post_type_frame = PostTypeFrame(header_frame, upload_type_frame)
        post_type_frame.grid(row=0, column=0, padx=10, pady=10)
        post_theme_frame = PostThemeFrame(header_frame)
        post_theme_frame.grid(row=0, column=1, padx=10, pady=10)

        body_frame = tk.Frame(self, background=style.widget_background)
        body_frame.pack(pady=10)
        post_title_frame = PostTitleFrame(body_frame)
        post_title_frame.pack(fill='x', padx=10,pady=10)
        post_caption_frame = PostCaptionFrame(body_frame)
        post_caption_frame.pack(fill="x", padx=10,pady=10)

        
        upload_type_frame.pack(fill='x', pady=10)
        
class PostTypeFrame(tk.Frame):
    def __init__(self, container, upload_type_frame: UploadTypeFrame):
        super().__init__(container)
        style = BaseStyle()
        self.upload_type_frame = upload_type_frame
        self.config(background=style.widget_background)
        type_info = (
        "The Post Type Determines what type of media is present in your post.\n" \
        "Use the Gallery Post to include multiple Images, Videos, or blocks of text")
        selectable_types = ["Select Post Type", "Text Post", "Image Post", "Video Post", "Gallery Post"]
        label = Label(self, text="Post Type:", font_size = TEXT_FONT_SIZE)
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
    def __init__(self, container):
        super().__init__(container)
        style = BaseStyle()
        self.config(background=style.widget_background)
        type_info = (
            "Select a Theme for your post. Themes html files can be modified for personal customization.\n"
            "Select the open button to view the selected theme")
        selectable_types = ["base.html"]
        print("TODO get list of available themes")
        label = Label(self, text="Post Theme:", font_size = TEXT_FONT_SIZE)
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
    def __init__(self, container):
        super().__init__(container)
        header = tk.Frame(self)
        header.pack(fill='x')
        label = Label(header, "Post Title:", TEXT_FONT_SIZE)
        label.pack(side='left')
        info_icon = InfoIconLight(header, "Enter Post Title. Title is limited to a single line.", INFO_ICON_SIZE)
        info_icon.pack(side='left', padx=3)
        self.title_entry = Entry(self, width = 75, font_size=14)
        self.title_entry.pack(side='left')

class PostCaptionFrame(tk.Frame):
    def __init__(self, container):
        super().__init__(container)
        header = tk.Frame(self)
        header.pack(fill='x')
        label = Label(header, "Post Caption:", TEXT_FONT_SIZE)
        label.pack(side='left')
        info_icon = InfoIconLight(header, "Enter Post Caption. Can include multiple paragraphs", INFO_ICON_SIZE)
        info_icon.pack(side='left', padx=3)
        self.caption_entry = ScrollText(self, width=75, height=12, font_size=14)
        self.caption_entry.pack(side='left')

class ImageUploadFrame(tk.Frame):
     def __init__(self, container):
        super().__init__(container)
        test = Label(self, "hello")
        test.pack()

class NewPost(tk.Frame):
    def __init__(self, container, main_window):
        super().__init__(container)
        FONT_SM = font.Font(family="Helvetica", size=10)
        FONT_MD = font.Font(family="Helvetica", size=14)
        FONT_LG = font.Font(family="Helvetica", size=16)
        self.main_window:tk.Frame = main_window
        self.media = []
        self.tk_images = []
        self.post_components:list = FileController.get_post_component_basenames()
        self.post_component_paths = FileController.get_post_component_paths()
        self.post_option = tk.StringVar(self)
        self.post_component_basename = JsonController.get_post_component_basename()
        self.post_component_path = JsonController.get_config_data("post_component")


        #GROUPER FRAMES
        self.config(bg=C1)
        self.main_frame = tk.Frame(self, bg=C1)
        self.main_frame.pack(fill='both', padx=10, pady=10)
        self.body_frame = tk.Frame(self.main_frame, bg=C1)
        self.body_frame.columnconfigure(0, weight=1)
        self.body_frame.columnconfigure(1, weight=1)
        self.body_frame.pack(fill='both', expand= True)
       
        #BODY
            #BODY LEFT
        body_left_frame = tk.Frame(self.body_frame, bg=C2)
        body_left_frame.grid(column=0, row=0, sticky=tk.NSEW, ipadx=5, ipady=5, padx=10,pady=10)
        media_list= MediaList(
            body_left_frame, 
            self.media, 
            self.tk_images)
        get_media_btn = GetMediaBtn(
            body_left_frame, 
            self.media, 
            self.tk_images, 
            media_list, 
            max_items=MAX_MEDIA_ITEMS)
        get_media_btn.pack(padx=10, pady=10, fill="x")
        media_list.pack()

            #BODY RIGHT
        body_right_frame = tk.Frame(self.body_frame, bg=C2)
        body_right_frame.columnconfigure(0, weight=1)
        body_right_frame.columnconfigure(1, weight=3)
        body_right_frame.grid(column=1, row=0, ipadx=5, sticky=tk.NSEW, padx=10, pady=10)
        
        post_option_style = ttk.Style(self)
        post_option_style.configure('Custom.TMenubutton', font=FONT_LG, width = 25, background="white", relief = "solid", borderwith = 3, bordercolor='SystemButtonFace')
        post_option_lbl = tk.Label(body_right_frame, text="Post Component:", bg=C2, font=FONT_SM)
        post_option_lbl.grid(column=0,row=0, sticky=tk.E, pady=2)
        post_option_menu = ttk.OptionMenu(
            body_right_frame,
            self.post_option,
            self.post_component_basename,
            *self.post_components,
            command= lambda value: JsonController.set_post_component(basename=value)
        )
        post_option_menu.config(style='Custom.TMenubutton')
        post_option_menu["menu"].config(font=FONT_MD, bg="white")
        post_option_menu.grid(column=1, row=0, sticky=tk.NW, pady=10, padx=(30,0))

        title_field_label = tk.Label(body_right_frame, text = "Title:", bg=C2, font=FONT_SM)
        title_field_label.grid(column=0, row=1, sticky=tk.E)
        self.title_field = TextField(body_right_frame, 1)
        self.title_field.grid(column=1,row=1, sticky=tk.N, pady=10)

        caption_field_label = tk.Label(body_right_frame, text = "Caption:", bg=C2, font=FONT_SM)
        caption_field_label.grid(column=0, row=2, sticky=tk.NE, pady=30)
        self.caption_field = TextField(body_right_frame, field_height=CAPTION_FEILD_HEIGHT)
        self.caption_field.grid(column=1,row=2, sticky=tk.N,pady=30)

        #Footer
        footer_frame = tk.Frame(self.main_frame, bg=C1)
        footer_frame.pack(expand=True, fill='x', padx=10, pady=10)
        build_post_font = font.Font(family="Helvetica", size=15, weight="bold")
        build_post_btn = tk.Button(
            footer_frame, 
            text="Build Post", 
            command=self.build_post, 
            font=build_post_font, 
            bg=C4,
            width=20)
        build_post_btn.pack(side="right")

        column_span_lbl = tk.Label(footer_frame, text="Column Span:", bg=C1)
        column_span_lbl.pack(side="left")
        self.column_span = tk.StringVar(value=1)
        column_span_spinbox = ttk.Spinbox(footer_frame, from_=1, to=10, textvariable=self.column_span, wrap=True, width=4)
        column_span_spinbox.pack(side='left')
        
    def get_caption_text(self)->str:
        caption = self.caption_field.get_text()
        if caption.endswith("\n"):
            caption = caption[:-1]
        return caption
    
    def get_title_text(self)->str:
        title = self.title_field.get_text()
        if title.endswith("\n"):
            title = title[:-1]
        return title

    def build_post(self):
        webpage = Webpage(html_path=Controller.get_resource_paths("html_webpage"))
        theme = Theme("themes/default.html")
        print("TODO: new_post.py build_post2(). Default theme is hardcoded. allow user to select a theme")
        post:Post = self.aquire_post_data()
        renderer = PostHtmlRenderer(post, theme)
        html_post = renderer.render()
        webpage.insert_html_post(html_post)
        self.append_posts_json(post)
 
    def aquire_post_data(self):
        post = Post(JsonController.get_config_data("base_link"))
        post.title = self.get_title_text()
        post.caption = self.get_caption_text()
        post.media_paths = FileController.add_media_to_assets_folder(self.media)
        print("TODO: assuming media is a single image. expand compatible media types")
        post.username = JsonController.get_config_data("username")
        post.profile_pic = JsonController.get_config_data("profile_pic")
        post.email = JsonController.get_config_data("email")
        post.links = []
        print("TODO: links not implemented. expand compatible media types")
        post.set_unique_id(JsonController.get_posts_data())
        return post

    def append_posts_json(self, post:Post):
        posts_data = JsonController.get_posts_data()
        new_post_data = post.get_json_post()
        JsonController.set_posts_data(posts_data.update(new_post_data))


def delete_media(post_html:bs):
    media_tag = post_html.find("img", attrs={"data-type": "media"})
    media_tag.extract()