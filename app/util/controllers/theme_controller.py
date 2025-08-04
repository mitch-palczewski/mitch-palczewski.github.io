import os

from app.util.controller import Controller
THEME_FOLDER_PATH = Controller.get_resource_paths("theme_folder")


class ThemePaths:
    @staticmethod
    def get_basenames() -> list:
            basenames = os.listdir(THEME_FOLDER_PATH)
            return basenames

    @staticmethod
    def get_all_paths() -> list:
        basenames = ThemePaths.get_basenames()
        paths:list = []
        for basename in basenames:
            path = os.path.join(THEME_FOLDER_PATH, basename)  
            paths.append(path)
        return paths

    @staticmethod
    def get_path(basename:str):
        path:str = os.path.join(THEME_FOLDER_PATH, basename)
        return path
    
    @staticmethod
    def get_local_path(basename:str):
         return os.path.join('themes', basename)