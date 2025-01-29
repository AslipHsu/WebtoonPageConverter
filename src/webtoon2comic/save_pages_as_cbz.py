import os
import zipfile
from pathlib import Path

from PIL.Image import Image as ImageType


def save_pages_as_cbz(
    pages: list[ImageType], output_file: Path, temp_dir: Path
) -> None:
    """Save all arranged pages as a CBZ file."""
    if temp_dir is None:
        temp_dir = Path(tempfile.gettempdir())

    # Ensure temp_dir exists
    temp_dir.mkdir(parents=True, exist_ok=True)

    with zipfile.ZipFile(output_file, "w") as cbz:
        for i, page in enumerate(pages):
            image_name = f"page_{i + 1:03}.jpg"
            temp_file_path = temp_dir / image_name
            page.save(temp_file_path, "JPEG")
            cbz.write(temp_file_path, arcname=image_name)
            os.remove(temp_file_path)
