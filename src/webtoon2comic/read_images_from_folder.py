from PIL.Image import Image as ImageType
from pathlib import Path
from PIL import Image


def read_images_from_folder(input_folder: Path) -> list[ImageType]:
    """Read all image files from a folder."""
    images: list[ImageType] = []
    for file_name in sorted(input_folder.iterdir()):
        if file_name.suffix.lower() in {".png", ".jpg", ".jpeg"}:
            with Image.open(file_name) as image:
                images.append(image.copy())
    return images
