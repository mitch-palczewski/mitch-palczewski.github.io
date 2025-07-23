from bs4 import BeautifulSoup as bs

from util.controller import PathsController

class Webpage:
    """
    Parameters 
        html_path
        html
        posts_div
    """
    def __init__(self, webpage_html_path:str = None):
        self.html_path = webpage_html_path or PathsController.get_path("webpage_html")
        self.html = self.open_html(self.html_path)
        self.posts_div = self.html.find("div", id="posts")

    @staticmethod 
    def open_html(path:str):
        with open(path, "r", encoding="utf-8") as file:
            html = bs(file, "html.parser")
        if not html:
            raise ValueError(f"Error: webpage file not found {path}")   
        return html