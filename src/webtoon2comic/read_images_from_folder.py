from pathlib import Path

from PIL import Image
from PIL.Image import Image as ImageType

import re

def read_images_from_folder(input_folder: Path) -> list[ImageType]:
    """Read all image files from a folder."""
    images: list[ImageType] = []
    for file_name in sorted(input_folder.iterdir(), key=lambda x: int(re.search(r'\d+', x.name).group())):
        if file_name.suffix.lower() in {".png", ".jpg", ".jpeg"}:
            with Image.open(file_name) as image:
                images.append(image.copy())
    return images
