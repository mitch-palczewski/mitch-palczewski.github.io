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
    
    @staticmethod
    def get_tkinter_filetypes(images: bool, videos: bool):
        """
        Build a tkinter filetypes tuple based on boolean flags.

        Args:
            include_images: If True, include image extensions.
            include_videos: If True, include video extensions.

        Returns:
            A tuple of (description, pattern) pairs, always ending
            with ("All files", "*.*").
        """
        filetypes = []
        if images:
            image_pattern = ";".join(f"*{ext}" for ext in sorted(VALID_HTML_IMAGE_EXTENSIONS))
            filetypes.append(("Image Files", image_pattern))

        if videos:
            video_pattern = ";".join(f"*{ext}" for ext in sorted(VALID_HTML_VIDEO_EXTENSIONS))
            filetypes.append(("Video Files", video_pattern))
        filetypes.append(("All files", "*.*"))
        return tuple(filetypes)

