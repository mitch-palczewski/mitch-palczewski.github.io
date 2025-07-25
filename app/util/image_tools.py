from PIL import Image, ImageTk
from app.util.controller import Controller

def load_icon(name: str, height: int) -> ImageTk.PhotoImage:
    """Load and resize an icon by filename and target height, preserving aspect ratio."""
    path = Controller.get_app_assets(name)
    img = Image.open(path)
    
    aspect_ratio = img.width / img.height
    target_width = int(height * aspect_ratio)

    resized_img = img.resize((target_width, height), Image.LANCZOS)
    return ImageTk.PhotoImage(resized_img)
