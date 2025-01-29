from PIL import Image, ImageOps
from PIL.Image import Image as ImageType


def arrange_panels_into_page(
    panels: list[ImageType],
    page_width: int = 1200,
    page_height: int = 1800,
    columns: int = 2,
    rows: int = 3,
    reading_order: str = "right-to-left",  # Options: 'right-to-left', 'left-to-right'
) -> ImageType:
    """Arrange panels into a single page with multiple rows and columns."""
    # Calculate each panel's size to fit in the grid
    panel_width = page_width // columns
    panel_height = page_height // rows

    # Create a blank page
    page = Image.new("RGB", (page_width, page_height), "white")

    # Adjust panel order based on reading direction
    if reading_order == "right-to-left":
        panels = list(reversed(panels))

    # Place panels in grid
    for i, panel in enumerate(panels):
        if i >= columns * rows:
            break  # Stop if panels exceed the grid size

        col = i % columns
        row = i // columns

        # Adjust column index for right-to-left reading
        if reading_order == "right-to-left":
            col = columns - 1 - col

        # Calculate position
        x = col * panel_width
        y = row * panel_height

        # Resize panel to fit grid cell
        panel_resized = ImageOps.pad(panel, (panel_width, panel_height), color="white")
        page.paste(panel_resized, (x, y))

    return page
