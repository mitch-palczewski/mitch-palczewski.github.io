from pathlib import Path

VALID_HTML_VIDEO_EXTENSIONS = {".mp4", ".webm", ".ogv", ".ogg"}
VALID_HTML_IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".pjpeg", ".pjp", ".jfif", ".png", ".gif",
                           ".svg", ".webp", ".avif", ".apng", ".ico", ".cur", ".bmp"}

class Extensions:
    @staticmethod
    def is_valid_html_video(filename: str) -> bool:
        suffix = Path(filename).suffix.lower()
        return suffix in VALID_HTML_VIDEO_EXTENSIONS
    
    @staticmethod
    def is_valid_html_image(filename: str) -> bool:
        suffix = Path(filename).suffix.lower()
        return suffix in VALID_HTML_IMAGE_EXTENSIONS