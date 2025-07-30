from app.gui.widgets.buttons import Button
from app.gui.widgets.frames import WidgetFrame

from app.util.controller import Controller, JsonController, FileController
from app.util.models.post import Post
from app.util.models.theme import Theme
from app.util.models.webpage import Webpage
from app.util.view.post_to_html import PostHtmlRenderer
from app.util.controllers.extensions import Extensions

class BuildPostButton(WidgetFrame):
    def __init__(self, container):
        super().__init__(container)
        button = Button(self, command=self.build_post, text="hello")
        button.pack()

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
    
