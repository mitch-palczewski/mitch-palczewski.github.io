from bs4 import BeautifulSoup as bs
from pathlib import Path
import copy
from app.util.models.post import Post, VALID_POST_TYPES
from app.util.models.theme import Theme
from app.util.controllers.extensions import Extensions, VALID_HTML_IMAGE_EXTENSIONS, VALID_HTML_VIDEO_EXTENSIONS


class PostHtmlRenderer:
    """
    Parameters 
        post: Post 
        webpage: Webpage
        theme: Theme
    Functions 
        render() -> None 
    """
    def __init__(self, post:Post, theme:Theme):
        self.post:Post = post 
        self.theme:Theme = theme
        self.post_html:bs = None
    
    def render(self) -> bs:
        post_type = self.post.type
        if post_type == "text":
            self.render_text()
        elif post_type == "image":
            self.render_image()
        elif post_type == "video":
            self.render_video()
        elif post_type == "gallery":
            self.render_gallery()
        else:
            print(f"Post HTML Renderer recieved invalid post type {post_type}. \
                Post Type should be {VALID_POST_TYPES}")
        print("TODO implement writing html")
        return self.post_html
        
    
    def render_text(self):
        self.post_html:bs = self.theme.text_post_html
        self.insert_post_id(self.post_html, self.post.id)
        self.insert_title(self.post_html, self.post.title)
        self.insert_date(self.post_html, self.post.datetime)
        self.insert_caption(self.post_html, self.post.caption)
    
    def render_image(self):
        self.post_html:bs = self.theme.image_post_html
        self.insert_post_id(self.post_html, self.post.id)
        self.insert_title(self.post_html, self.post.title)
        self.insert_date(self.post_html, self.post.datetime)
        self.insert_caption(self.post_html, self.post.caption)
        self.insert_image(self.post_html, self.post.media_paths)

    def render_video(self):
        self.post_html:bs = self.theme.video_post_html
        self.insert_post_id(self.post_html, self.post.id)
        self.insert_title(self.post_html, self.post.title)
        self.insert_date(self.post_html, self.post.datetime)
        self.insert_caption(self.post_html, self.post.caption)
        self.insert_video(self.post_html, self.post.media_paths)
        
    def render_gallery(self):
        self.post_html:bs = self.theme.gallery_post_html
        self.insert_post_id(self.post_html, self.post.id)
        self.insert_title(self.post_html, self.post.title)
        self.insert_date(self.post_html, self.post.datetime)
        self.insert_caption(self.post_html, self.post.caption)
        self.insert_gallery_media(self.post_html, self.post.media_paths)

    @staticmethod
    def insert_post_id(html:bs, id:str):
        tag = html.find(attrs={"data-post_id": True})
        if tag: 
            tag["data-post_id"] = id
        else: 
            html.attrs["data-post_id"] = id

    @staticmethod
    def insert_title(html:bs, title:str):
        tag = html.find(attrs={"data-type": "title"})
        if title == "":
            tag.decompose()
            return
        tag.clear()
        tag.insert(0, title)

    @staticmethod
    def insert_date(html:bs, date:str):
        tag = html.find(attrs={"data-type": "date"})
        tag.clear()
        tag.insert(0, date)

    @staticmethod
    def insert_caption(html:bs, caption:str):
        tag = html.find(attrs={"data-type": "caption"})
        if caption == "":
            tag.decompose()
            return
        tag.clear()
        tag.insert(0, caption)

    @staticmethod
    def insert_links(html:bs, links:list):
        container = html.find("div", attrs={"data-type": "link_container"})
        if len(links) == 0:
            container.decompose()
            return
        first_link = container.find("a")
        link_template = copy.deepcopy(first_link)
        container.clear(decompose=True)
        for link, text in links:
            new_link = copy.deepcopy(link_template)
            new_link["src"] = link
            if text == "":
                new_link.insert(link)
            new_link.insert(text)
            container.insert(0, new_link)

    @staticmethod
    def insert_image(html:bs, image_links:list):
        image_src = image_links[0]
        tag = html.find(attrs={"data-type": "image"})
        tag["src"] = image_src

    @staticmethod
    def insert_video(html:bs, video_links:list):
        video_src = video_links[0]
        tag = html.find(attrs={"data-type": "video_source"})
        tag["src"] = video_src

    @staticmethod
    def insert_gallery_media(html:bs, gallery_links:list):
        gallery_links.reverse()
        first_image:bs = html.find("img", attrs={"data-type": "image"})
        first_video:bs = html.find("video", attrs={"data-type": "video"})
        image_template:bs = copy.deepcopy(first_image)
        video_template:bs = copy.deepcopy(first_video)
        gallery:bs = html.find(attrs={"data-type": "gallery"})
        gallery.decompose()
        for link in gallery_links:
            if Extensions.is_valid_html_video(link):
                new_video = copy.deepcopy(video_template)
                new_video_source = new_video.find("source", attrs={"data-type": "video_sourc"})
                new_video_source["src"] = link
                gallery.insert(0, new_video)
                continue
            if Extensions.is_valid_html_image(link):
                new_image = copy.deepcopy(image_template)
                new_image["src"] = link
                gallery.insert(0, new_image)
            print(f"WARNING: Invalid Link Extentions: {link}. \
                  Accepted Extentions are video {VALID_HTML_VIDEO_EXTENSIONS} and image {VALID_HTML_IMAGE_EXTENSIONS}")





            
            

        
 