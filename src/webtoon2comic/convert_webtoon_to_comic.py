from pathlib import Path

from PIL.Image import Image as ImageType

from .arrange_panels_into_page.arrange_panels_into_page import arrange_panels_into_page
from .read_images_from_folder import read_images_from_folder
from .save_pages_as_cbz import save_pages_as_cbz
from .split_webtoon_image.split_webtoon_image import split_webtoon_image
from .split_webtoon_image.split_webtoon_image2 import split_webtoon_image_by_cut_space

def convert_webtoon_to_comic(
    input_folder: Path,
    output_file: Path,
    temp_dir: Path,
    panel_height=1000,
    page_width=1200,
    page_height=1800,
    columns=2,
    rows=3,
    reading_order="right-to-left",
    split="fixed-size",#fixed-size, cut-space
) -> None:
    """Main function to convert webtoon format to traditional comic format."""
    images = read_images_from_folder(input_folder)
    all_pages: list[ImageType] = []

    for image in images:
        # Split the image into multiple panels
        if split=="fixed-size":
            panels = split_webtoon_image(image, panel_height=panel_height)
        elif split=="cut-space":
            panels = split_webtoon_image_by_cut_space(image)
        else:
            panels = split_webtoon_image(image, panel_height=panel_height)
        # Arrange all panels into pages
        for i in range(0, len(panels), columns * rows):
            page_panels = panels[i : i + columns * rows]
            page = arrange_panels_into_page(
                page_panels,
                page_width=page_width,
                page_height=page_height,
                columns=columns,
                rows=rows,
                reading_order=reading_order,
            )
            all_pages.append(page)

    # Save all pages as a CBZ file
    save_pages_as_cbz(all_pages, output_file, temp_dir)
