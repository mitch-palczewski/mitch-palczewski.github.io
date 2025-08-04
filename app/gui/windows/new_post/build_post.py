import os
import shutil
import tkinter as tk
from app.gui.widgets.buttons import Button
from app.gui.widgets.frames import WidgetFrame
from app.gui.widgets.labels import WidgetLabel

from app.util.controller import Controller, JsonController
from app.util.models.post import Post
from app.util.models.theme import Theme
from app.util.models.webpage import Webpage
from app.util.view.post_to_html import PostHtmlRenderer
from app.util.controllers.post_controller import PostController

class BuildPostButton(WidgetFrame):
    def __init__(self, container, post_controller:PostController):
        super().__init__(container)
        button = Button(self, command=self.build_post, text="Build Post", fontsize=18)
        button.pack(fill='x', pady=10)
        self.post_controller = post_controller

    def build_post(self):
        webpage = Webpage(html_path=Controller.get_resource_paths("html_webpage"))
        theme = Theme("themes/base.html")
        print("TODO: new_post.py build_post2(). Default theme is hardcoded. allow user to select a theme")
        post:Post = self.aquire_post_data()
        renderer = PostHtmlRenderer(post, theme)
        html_post = renderer.render()
        webpage.insert_html_post(html_post)
        self.append_posts_json(post)
        self.after_post_built()
 
    def aquire_post_data(self):
        """
        Builds Post Object
        """
        post = Post(JsonController.get_config_data("base_link"))
        post.title = self.post_controller.title_entry.get()
        post.caption = self.post_controller.caption_entry.get_all()
        post.type = self.post_controller.post_type
        post.links = self.post_controller.link_collection.get_all_links()
        if post.type != 'text':
            post.local_media = self.post_controller.media_collection.get_media_list()
        post.username = JsonController.get_config_data("username")
        post.profile_pic = JsonController.get_config_data("profile_pic")
        post.email = JsonController.get_config_data("email")
        post.set_unique_id(JsonController.get_posts_data())
        return post

    def append_posts_json(self, post:Post):
        post_id = post.id
        posts_data = JsonController.get_posts_data()
        new_post_data = post.get_post_as_json()
        if posts_data:
            posts_data[post_id] = new_post_data[post_id]
            JsonController.set_posts_data(posts_data)
        else:
            JsonController.set_posts_data(new_post_data)

    def after_post_built(self):
        Controller.web_page_change()
        PostBuiltPopUp(self.post_controller.main_window.body_frame, self.post_controller)

class PostBuiltPopUp(tk.Toplevel):
    def __init__(self, parent, post_controller:PostController, width=600, height=600, alpha=0.8, **kwargs):
        super().__init__(parent, **kwargs)
        self.attributes('-topmost', True)
        self.grab_set()
        self.configure(bg='black')
        self.attributes('-alpha', alpha)
        self.overrideredirect(True)
        self.geometry(f"{parent.winfo_width()}x{parent.winfo_height()}+{parent.winfo_rootx()}+{parent.winfo_rooty()}")

        self.frame = tk.Frame(self, width=width, height=height)
        self.frame.place(relx=0.5, rely=0.5, anchor='center')

        self.post_controller = post_controller
        lbl  = WidgetLabel(self.frame, "Post Successfully Built.")
        lbl.pack(padx=3, pady=10, fill='x')
        load_main_window_btn = Button(self.frame,self.load_main_window, "Return to Landing Page")
        load_main_window_btn.pack(padx=3, pady=10, fill='x')
        load_new_post_window_btn = Button(self.frame,self.load_new_post_window, "Make another post")
        load_new_post_window_btn.pack(padx=3, pady=10, fill='x')
        
    def load_main_window(self):
        main_window = self.post_controller.main_window
        main_window.load_content("Landing")
        self.destroy()
    
    def load_new_post_window(self):
        main_window = self.post_controller.main_window
        main_window.load_content("NewPost")
        self.destroy()