from datetime import datetime
from urllib.parse import urlparse, quote, urljoin
import os
import json
from app.util.extensions import Extensions
VALID_POST_TYPES = ["text", "image", "video", "gallery"]
class Post():   
    """
    Args Manually Set: 
        base_link: str
        title:str 
        caption:str     
        local_media: ['assets//url1.mp4', 'assets//utl2.png', "hello world", ...]
        base_link: str url 
        username: str
        profile_pic: str url
        email: str email
        links: [('url1', 'text1'), ('url2', 'text2'), ...]
    
    Args Automatically Set:
        json_media: list ['ww.baselink.com/assets/url1.mp4', 'ww.baselink.com/assets/utl2.png', ...]
        type: str "text_post", "image_post", "video_post", "gallery_post"
        datetime: str "2025-07-24 15:30:00"

    Functions:
        set_unique_id(existing_ids:list)
            Finds a unique id from a list of ids 
        get_post_as_json() -> str {'000003':{'datetime': '01/25/25', 'title': 'new post title', ...}}
            Returns Post in Json form        
    """
    def __init__ (self, base_link):
        # MANUALLY SET
        self.base_link:str = base_link
        self.id:str = ""
        self.title:str = "" 
        self._caption:str = ""
        self._local_media:list = []
        self.username:str = ""
        self.profile_pic:str = ""
        self.email:str = ""
        self._links:list = []

        #AUTOMATICALLY SET
        self.json_media:list = []
        self.json_link:list = []
        self.type:str = None
        self.datetime:str = str(datetime.now())
    
    @property
    def caption(self):
        return self._caption
    @caption.setter
    def caption(self, value:str):
        self._caption = value
        self.set_post_type()
  
    @property
    def local_media(self):
        return self._local_media
    @local_media.setter
    def local_media(self, value:list):
        value = PostUtil.validate_media_list(value)
        self._local_media = value
        self.set_post_type()   
        self.format_local_media_for_json(self.json_media, value)

    @property
    def links(self):
        return self._links
    @links.setter
    def links(self, value:list):
        if not PostUtil.is_list_of_pairs(value):
            ValueError(f"Links are not a list of pairs. Each element should be ('url', text). You entered {value}")
        self._links = value

    def get_post_as_json(self) -> str:
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
        json_data = {self.id : {
            "datetime": self.datetime,
            "title": self.title,
            "caption": self._caption,
            "media_links": self.json_media,
            "base_link": self.base_link,
            "username": self.username,
            "profile_pic": self.profile_pic,
            "email": self.email,
            "links": self.format_links_for_json(self.links)
            }
        }
        return json_data
    
    def set_unique_id(self, posts:dict):
        """
        Parameter
            posts: dict
            A deserialized Json file where the keys are are integers.  
        """
        if posts:
            self.id = PostUtil.find_unique_id(posts.keys())
        else:
            self.id = '000001'

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
            and len(self._local_media) == 0 
            ):
            self.type = "text"
        elif(
            len(self._local_media) == 1
            and Extensions.is_valid_html_image(self._local_media[0])
            ):
            self.type = "image"
        elif(
            len(self._local_media) == 1
            and Extensions.is_valid_html_video(self._local_media[0])
            ):
            self.type = "video"
        elif(
            len(self._local_media) > 1
            ):
            self.type = "gallery"
    
    def format_links_for_json(self, links:list):
        self.json_link = []
        for link, text in links:
            link_dict = {"link":link,"text":text}
            self.json_link.append(link_dict)
        return self.json_link
    
    def format_local_media_for_json(self, json_media:list, media:list):
        """
        Turns local image or video paths into web urls
        Args:
            json_media: list = self.image_links or self.video_links or self.gallery_links
            media: list = list of local paths for images or video or gallery media
        """
        for element in media:
            if Extensions.is_valid_html_image(element) or Extensions.is_valid_html_image(element):
                url = PostUtil.build_web_asset_url(self.base_link, element)
                json_media.append(url)
            else:
                json_media.append(element)
        
    def validate_post(self):
        if self.id == "" or len(self.id) != 6:
            ValueError("id is not set. set_unique_id(existing_ids)", self.id)
        if (self._caption == "" 
            and len(self._local_media) == 0 ):
            self.type = None
            print("WARNING: Post does not contain content. " \
            "Set the caption:str, image_links:[urls], video_links:[urls]")
        for media in self._local_media:
            if (type(media) != str):
                print(f"WARNING: media must be a string {media}")
        if (self.title == ""):
            print(f"Warning: Post {self.id} title is blank")
    

class PostUtil:
    @staticmethod
    def validate_media_list(media:list):
        for element in media:
            if type(element) is not str:
                print(f"WARNING {element} is not a string. This item will be removed")
                media.remove(element)
        return media
    
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
    
    @staticmethod
    def build_web_asset_url(base_url: str, local_path: str) -> str:
        """
        Convert a local file path to a properly encoded web URL.

        Args:
            base_url (str): The root URL of the site (e.g. "https://example.com/")
            local_path (str): Relative local path to the asset (e.g. "assets\\My File.png")

        Returns:
            str: Fully-qualified URL pointing to the asset

        Raises:
            ValueError: If base_url or local_path is missing or invalid
        """
        if not base_url or not isinstance(base_url, str):
            raise ValueError("Missing or invalid base_url")
        if not local_path or not isinstance(local_path, str):
            raise ValueError("Missing or invalid local_path")
        try:
            web_path = local_path.replace("\\", "/")
            folder, filename = os.path.split(web_path)
            encoded_filename = quote(filename)
            encoded_path = f"{folder}/{encoded_filename}" if folder else encoded_filename
            full_url = urljoin(base_url, encoded_path)
            return full_url
        except Exception as e:
            raise ValueError(f"Failed to build URL: {e}")
        
    



