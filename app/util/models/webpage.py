from bs4 import BeautifulSoup as bs

from app.util.controller import PathsController

class Webpage:
    """
    Parameters 
        html_path
        html
        posts_div
    """
    def __init__(self, html_path:str = None):
        self.html_path = html_path or PathsController.get_path("webpage_html")
        self.html = self.open_html(self.html_path)
        self.posts_div = self.html.find("div", id="posts")

    def insert_html_post(self, html_post:bs):
        posts_container = self.html.find(attrs={"data-type": "posts_container"})
        if posts_container is None:
            raise ValueError("Error: Could not find posts container with data-type='posts_container'")
        try:
            posts_container.insert(0, html_post)
            self.write_html_file(self.html_path, self.html)
        except Exception as e:
            raise RuntimeError(f"Error inserting html_post: {e}")

    @staticmethod 
    def open_html(path:str):
        with open(path, "r", encoding="utf-8") as file:
            html = bs(file, "html.parser")
        if not html:
            raise ValueError(f"Error: webpage file not found {path}")   
        return html
    
    @staticmethod
    def write_html_file(path:str, data:bs) -> None:
        with open(path, "w", encoding="utf-8") as file:
            file.write(str(data))
