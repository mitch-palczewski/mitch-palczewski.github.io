class NewPostController:
    def __init__(self):
        self._post_type:str = None
        self.theme_selector = None
        self.title_entry = None
        self.caption_entry = None
        self.media_entry = None
    
    @property
    def post_type(self):
        return self._post_type
    
    @post_type.setter
    def post_type(self, value):
        if value is not "text" or 'image' or 'video' or 'gallery':
            raise ValueError(value, "Post Type must be text, image, video, or gallery")
        self._post_type = value

        
