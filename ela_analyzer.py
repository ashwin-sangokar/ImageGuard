from pathlib import Path
from PIL import Image, ImageChops, ImageEnhance
import io

def generate_ela(image_path, output_path, quality=90, scale=10):
    """
    Generate an Error Level Analysis visualization for JPEG images.
    ELA is an investigative aid, not a reliable standalone forgery detector.
    """
    with Image.open(image_path) as original:
        if original.format not in ("JPEG", "JPG"):
            raise ValueError("ELA is enabled for JPEG images only. Select a .jpg or .jpeg file.")
        original = original.convert("RGB")
        buffer = io.BytesIO()
        original.save(buffer, "JPEG", quality=quality)
        buffer.seek(0)
        recompressed = Image.open(buffer).convert("RGB")
        difference = ImageChops.difference(original, recompressed)
        difference = ImageEnhance.Brightness(difference).enhance(scale)
        difference.save(output_path, "JPEG", quality=95)
    return str(Path(output_path))
