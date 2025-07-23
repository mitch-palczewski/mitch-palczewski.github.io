from datetime import datetime
from urllib.parse import urlparse
VALID_POST_TYPES = ["text", "image", "video", "gallery"]
class Post():   
    """
    Defines a PiePost Post. 
        Functions 
            set_unique_id(existing_ids:list)
                Finds a unique id from a list of ids 
            get_json_post()
                Returns Post in Json form 

        Variables to be set 
            title:str 
            caption:str     
            image_links: ['url1.png', 'url2.jpeg', ...] 
            video_links:  ['url1.mp4', 'url2.mp4', ...] 
            gallery_links: ['url1.mp4', 'utl2.png', ...]
            base_link: str url 
            username: str
            profile_pic: str url
            email: str email
            links: [('url1', 'text1'), ('url2', 'text2'), ...]
    """
    def __init__ (self):
        self.id:str = ""
        self.date:str = str(datetime.now())
        self.title:str = "" 
        self._caption:str = ""
        self._image_links:list = []
        self._video_links:list = []
        self._gallery_links:list = []
        self.base_link:str = ""
        self.username:str = ""
        self.profile_pic:str = ""
        self.email:str = ""
        self._links:list = []

        self.type:str = None
    
    @property
    def caption(self):
        return self._caption
    
    @caption.setter
    def caption(self, value:str):
        self._caption = value
        self.set_post_type()

    @property
    def image_links(self):
        return self._image_links
    
    @image_links.setter
    def image_links(self, value:list):
        value = Post.validate_url_list(value)
        self._image_links = value
        self.set_post_type()

    @property
    def video_links(self):
        return self._video_links
    
    @video_links.setter
    def video_links(self, value:list):
        value = Post.validate_url_list(value)
        self._video_links = value
        self.set_post_type()
    
    @property
    def gallery_links(self):
        return self._gallery_links
    
    @gallery_links.setter
    def gallery_links(self, value:list):
        value = Post.validate_url_list(value)
        self._video_links = value
        self.set_post_type()   

    @property
    def links(self):
        return self._links
    
    @links.setter
    def links(self, value:list):
        if not self.is_list_of_pairs(value):
            ValueError(f"Links are not a list of pairs. Each element should be ('url', text). You entered {value}")
        self._links = value

    def get_json_post(self) -> str:
        """
        Returns Post JSON data \n
        example json \n
        {'000001':
            {'date': '2025-07-18 12:33:31.998130', 
            'title': 'Cool Post', 
            'caption': 'This is a super cool piepost', 
            'image_links': ['ww.baselink.com/imageurl', ...], 
            'video_links': ['ww.baselink.com/videourl', ...], 
            'base_link': 'ww.baselink.com', 
            'username': 'cool-username', 
            'profile_pic': 'ww.baselink.com/ppimageurl', 
            'email': 'myemail@gmail..com'}
        }
        """
        self.validate_post()
        json = {self.id : {
            "date": self.date,
            "title": self.title,
            "caption": self._caption,
            "image_links": self.image_links,
            "video_links": self.video_links,
            "base_link": self.base_link,
            "username": self.username,
            "profile_pic": self.profile_pic,
            "email": self.email,
            "links": self._links
            }
        }
        return json
    
    def set_unique_id(self, posts:dict):
        """
        Parameter
            posts: dict
            A deserialized Json file where the keys are are integers.  
        """
        self.id = Post.find_unique_id(posts.keys())

    def set_post_type(self, type_override = None):
        """
        Automatically sets the type of post 
            [text, image, video, gallery]
        or can be overridden with the type_override parameter
        """
        if type_override:
            self.type = type_override
            return
        if (
            self.caption != "" 
            and len(self._image_links) == 0 
            and len(self._video_links) == 0
            ):
            self.type = "text"
        elif(
            len(self._image_links) == 1 
            and len(self._video_links) == 0
            ):
            self.type = "image"
        elif(
            len(self._image_links) == 0 
            and len(self._video_links) == 1
            ):
            self.type = "video"
        elif(
            (len(self._image_links) > 1 or len(self._video_links) > 1) 
            or (len(self._image_links) == 1 and len(self._video_links) == 1)
            or (len(self._gallery_links) > 0)
            ):
            self.type = "gallery"
        
    def render_html():
        pass
        
    def validate_post(self):
        if self.id == "" or len(self.id) != 6:
            ValueError("id is not set. set_unique_id(existing_ids)", self.id)
        if (self._caption == "" 
            and len(self.image_links) == 0 
            and len(self.video_links) == 0):
            self.type = None
            Warning("Warning: Post does not contain content. " \
            "Set the caption:str, image_links:[urls], video_links:[urls]")
        if (self.title == ""):
            Warning(f"Warning: Post {self.id} title is blank")

    @staticmethod
    def validate_url_list(urls:list):
        for url in urls:
            if type(url) is not str:
                Warning(f" {url} is not a string. This item will be removed")
                urls.remove(url)
            elif(not Post.is_url(url)):
                Warning(f" {url} is not a valid URL. This item will be removed")
                urls.remove(url)
        return urls
    
    @staticmethod
    def is_list_of_pairs(lst):
        return all(isinstance(item, tuple) and len(item) == 2 for item in lst)


    @staticmethod
    def is_url(string:str):
        parsed = urlparse(string)
        return bool(parsed.scheme) and bool(parsed.netloc)


    @staticmethod
    def find_unique_id(existing_ids):
        highest_id = 0
        for id in existing_ids:
            id_int = int(id)
            if id_int > highest_id:
                highest_id = id_int
        new_id = highest_id + 1
        return f"{new_id:06d}" 

  


