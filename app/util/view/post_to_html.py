from bs4 import BeautifulSoup as bs
from pathlib import Path
import copy
from app.util.models.post import Post, VALID_POST_TYPES
from app.util.models.webpage import Webpage
from app.util.models.theme import Theme

VALID_VIDEO_EXTENSIONS = {".mp4", ".webm", ".ogv", ".ogg"}
VALID_IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".pjpeg", ".pjp", ".jfif", ".png", ".gif",
                           ".svg", ".webp", ".avif", ".apng", ".ico", ".cur", ".bmp"}


class PostHtmlRenderer:
    """
    Parameters 
        post: Post 
        webpage: Webpage
        theme: Theme
    Functions 
        render() -> None 
    """
    def __init__(self, post:Post, webpage:Webpage, theme:Theme):
        self.post:Post = post 
        self.webpage:Webpage = webpage
        self.theme:Theme = theme
    
    def render(self):
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
        
    
    def render_text(self):
        html:bs = self.theme.text_post_html
        self.insert_post_id(html, self.post.id)
        self.insert_title(html, self.post.title)
        self.insert_date(html, self.post.date)
        self.insert_caption(html, self.post.caption)
    
    def render_image(self):
        html:bs = self.theme.image_post_html
        self.insert_post_id(html, self.post.id)
        self.insert_title(html, self.post.title)
        self.insert_date(html, self.post.date)
        self.insert_caption(html, self.post.caption)
        self.insert_image(html, self.post.image_links)

    def render_video(self):
        html:bs = self.theme.video_post_html
        self.insert_post_id(html, self.post.id)
        self.insert_title(html, self.post.title)
        self.insert_date(html, self.post.date)
        self.insert_caption(html, self.post.caption)
        self.insert_video(html, self.post.video_links)
        
    def render_gallery(self):
        html:bs = self.theme.gallery_post_html
        self.insert_post_id(html, self.post.id)
        self.insert_title(html, self.post.title)
        self.insert_date(html, self.post.date)
        self.insert_caption(html, self.post.caption)
        self.insert_gallery_media(html, self.post.image_links, self.post.video_links)

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
        tag.clear()
        tag.insert(0, caption)

    @staticmethod
    def insert_links(html:bs, links:list):
        container = html.find("div", attrs={"data-type": "link_container"})
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
            if PostHtmlRenderer.is_valid_html_video(link):
                new_video = copy.deepcopy(video_template)
                new_video_source = new_video.find("source", attrs={"data-type": "video_sourc"})
                new_video_source["src"] = link
                gallery.insert(0, new_video)
                continue
            if PostHtmlRenderer.is_valid_html_image(link):
                new_image = copy.deepcopy(image_template)
                new_image["src"] = link
                gallery.insert(0, new_image)
            print(f"WARNING: Invalid Link Extentions: {link}. \
                  Accepted Extentions are video {VALID_VIDEO_EXTENSIONS} and image {VALID_IMAGE_EXTENSIONS}")

    @staticmethod
    def is_valid_html_video(filename: str) -> bool:
        suffix = Path(filename).suffix.lower()
        return suffix in VALID_VIDEO_EXTENSIONS
    
    @staticmethod
    def is_valid_html_image(filename: str) -> bool:
        suffix = Path(filename).suffix.lower()
        return suffix in VALID_IMAGE_EXTENSIONS




            
            

        
 