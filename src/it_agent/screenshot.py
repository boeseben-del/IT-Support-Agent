"""Screenshot capture utilities."""

import io
from PIL import Image


def capture_screenshot():
    """Capture a full-screen screenshot and return it as bytes in a BytesIO buffer.
    
    Tries pyautogui first, then falls back to PIL.ImageGrab.
    Returns (BytesIO buffer, PIL.Image) or (None, None) on failure.
    """
    img = None
    try:
        import pyautogui
        img = pyautogui.screenshot()
    except Exception:
        try:
            from PIL import ImageGrab
            img = ImageGrab.grab()
        except Exception:
            return None, None

    if img is None:
        return None, None

    buf = io.BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    return buf, img


def image_to_thumbnail(img, max_height=150):
    """Resize a PIL Image to a thumbnail with the given max height, preserving aspect ratio."""
    if img is None:
        return None
    ratio = max_height / img.height
    new_width = int(img.width * ratio)
    return img.resize((new_width, max_height), Image.LANCZOS)
