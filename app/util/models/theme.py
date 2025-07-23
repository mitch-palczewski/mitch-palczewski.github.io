from bs4 import BeautifulSoup as bs

class Theme:
    """
    Parameters 
        path: File Path 
    Read Only Parameters 
        header_html: beautifulsoup
        footer_html: beautifulsoup
        text_post_html: beautifulsoup
        image_post_html: beautifulsoup
        video_post_html: beautifulsoup
        gallery_post_html: beautifulsoup
    Functions 
        new(name:str)
        host()
    Static Functions 
        open_html(path:str) -> beautifulsoup 
        write_html(path:str, html:beautifulsoup)
    """
    def __init__(self, path:str):
        self.path = path
        self.master_html = self.open_html(self.path)
        self._header_html = None
        self._footer_html = None
        self._text_post_html = None
        self._image_post_html = None 
        self._video_post_html = None
        self._gallery_post_html = None 

    @property 
    def header_html(self) -> bs:
        if self._header_html == None:
            self._header_html = self.master_html.find("header")
            if not self._header_html:
                Warning(f"Did not find <header> tag in theme {self.path}")
        return self._header_html 
    
    @property 
    def footer_html(self) -> bs:
        if self._footer_html == None:
            self._footer_html = self.master_html.find("footer")
            if not self._footer_html:
                Warning(f"Did not find <footer> tag in theme {self.path}")
        return self._footer_html 
    
    @property 
    def text_post_html(self) -> bs:
        if self._text_post_html == None:
            self._text_post_html = self.master_html.find("div", attrs={"data-type": "text_post"})
            if not self._text_post_html:
                Warning(f"Did not find <div data-type='text_post'> tag in theme {self.path}")
        return self._text_post_html 
    
    @property 
    def image_post_html(self) -> bs:
        if self._image_post_html == None:
            self._image_post_html = self.master_html.find("div", attrs={"data-type": "image_post"})
            if not self._image_post_html:
                Warning(f"Did not find <div data-type='image_post'> tag in theme {self.path}")
        return self._image_post_html 
    
    @property 
    def video_post_html(self) -> bs:
        if self._video_post_html == None:
            self._video_post_html = self.master_html.find("div", attrs={"data-type": "video_post"})
            if not self._video_post_html:
                Warning(f"Did not find <div data-type='video_post'> tag in theme {self.path}")
        return self._video_post_html 
    
    @property 
    def gallery_post_html(self) -> bs:
        if self._gallery_post_html == None:
            self._gallery_post_html = self.master_html.find("div", attrs={"data-type": "gallery_post"})
            if not self._gallery_post_html:
                Warning(f"Did not find <div data-type='gallery_post'> tag in theme {self.path}")
        return self._gallery_post_html 

    def new(name:str):
        NotImplementedError()

    def host(self):
        NotImplementedError()

    @staticmethod
    def open_html(path:str) -> bs:
        with open(path, "r", encoding="utf-8") as file:
            html = bs(file, "html.parser")
        if not html:
            raise ValueError(f"Error: file not found {path}")   
        return html
    
    @staticmethod
    def write_html_file(path:str, html:bs) -> None:
        with open(path, "w", encoding="utf-8") as file:
            file.write(str(html))