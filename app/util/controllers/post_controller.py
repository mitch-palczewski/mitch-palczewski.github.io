from app.gui.widgets.text import Text, ScrollText, Entry
from app.util.models.media import MediaCollection
from app.util.models.link import LinkCollection

class PostController:
    def __init__(self):
        self._post_type:str = None
        self.theme_selector = None
        self.title_entry:Entry = None
        self.caption_entry:ScrollText = None
        self._media_collection:MediaCollection = None
        self.link_collection:LinkCollection = None
        self.main_window = None
    
    @property
    def media_collection(self):
        if not self._media_collection:
            return MediaCollection()
        return self._media_collection
    @media_collection.setter
    def media_collection(self, value):
        self._media_collection = value 

    @property
    def post_type(self):
        return self._post_type
    @post_type.setter
    def post_type(self, value):
        if value != "text" and value != 'image' and value != 'video' and value != 'gallery':
            raise ValueError(value, "Post Type must be text, image, video, or gallery")
        self._post_type = value

        
