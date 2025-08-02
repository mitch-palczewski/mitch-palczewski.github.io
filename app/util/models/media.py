from dataclasses import dataclass
import os
import shutil
from app.gui.widgets.text import Text
from app.util.controller import Controller

@dataclass
class MediaObj:
    entry_type:str = None
    file_path:str = None
    tk_photoimage:str = None
    text:str = None
    text_obj:Text = None
    delete:bool = False

class MediaCollection:
    def __init__(self, max_items:int = None):
        self.max_entries = max_items
        self.entries = []
        self.tk_entries = []

    def get_media_list(self):
        media_list = []
        for entry in self.entries:
            if not isinstance(entry, MediaObj):
                raise ValueError(entry, "Entry must be a Media obj")
            if entry.delete:
                continue
            if entry.entry_type == 'text':
                media_list.append(entry.text_obj.get_all())
                continue
            else:
                new_path = add_media_to_assets_folder(entry.file_path)
                media_list.append(new_path)
        return media_list

def add_media_to_assets_folder(file_path):
    new_path:str = move_media_to_folder(file_path, Controller.get_resource_paths("assets_folder"))
    return new_path

def move_media_to_folder(media:str, folder_path:str) -> str:
        if not media:
            print("media does not exist")
            return ""
        if not folder_path:
            print("folder path does not exist")
            return ""
        shutil.copy(media, folder_path)
        file_name = os.path.basename(media)
        new_path = os.path.join(folder_path, file_name)
        return new_path
            