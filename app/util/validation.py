from app.util.controller import JsonController
from tkinter.messagebox import showwarning
from bs4 import BeautifulSoup as bs

class HtmlValidation:
    @staticmethod
    def validate_html(type:str, html:str):
        valid = True
        html_validation = JsonController.get_html_validation()
        required_data = html_validation[type]
        tags_not_found:list = HtmlValidation.get_tags_not_found(required_data, html)
        if len(tags_not_found) != 0:
            valid = False
            showwarning(title="Invalid HTML", message=f"Invalid HTML. \n Missing {tags_not_found}")
        return valid
    
    @staticmethod
    def get_tags_not_found(expected_tags:list, html:bs):
        tags_found = []
        tags_not_found = []
        if html is not type(bs):
            html = bs(html, "html.parser")
        for tag in html.find_all():
            data_type = tag.get("data-type")
            id = tag.get("id")
            for expected_tag in expected_tags:
                if data_type and expected_tag == data_type: 
                    tags_found.append(expected_tag)
                if id and expected_tag == id:
                    tags_found.append(expected_tag)
                if expected_tag == tag.name:
                    tags_found.append(expected_tag)
        
        for expected_tag in expected_tags:
            if not expected_tag in tags_found:
                tags_not_found.append(expected_tag)
        return tags_not_found