
from PIL.Image import Image as ImageType


def split_webtoon_image(image: ImageType, panel_height: int = 1000) -> list[ImageType]:
    """Split a webtoon image into smaller panels based on height."""
    width, height = image.size
    panels: list[ImageType] = []
    for top in range(0, height, panel_height):
        box = (0, top, width, min(top + panel_height, height))
        cropped_image = image.crop(box)
        panels.append(cropped_image)
    return panels
