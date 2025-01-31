from pathlib import Path

from .convert_webtoon_to_comic import convert_webtoon_to_comic


if __name__ == "__main__":
    # Example usage:
    # python -m venv .venv
    # .venv\\Scripts\\pip install pillow
    # .venv\\Scripts\\python webtoon2comic.py --input .\webtoon --output .\comic.cbz --temp-dir .\tmp

    import argparse

    parser = argparse.ArgumentParser(
        description="Convert Webtoon images to traditional comic format."
    )
    parser.add_argument(
        "--input",
        type=Path,
        required=True,
        help="Input folder containing Webtoon images.",
    )
    parser.add_argument(
        "--output", type=Path, required=True, help="Output CBZ file path."
    )
    parser.add_argument(
        "--panel-height", type=int, default=1000, help="Height of each panel."
    )
    parser.add_argument(
        "--page-width", type=int, default=1200, help="Width of comic page."
    )
    parser.add_argument(
        "--page-height", type=int, default=1800, help="Height of comic page."
    )
    parser.add_argument(
        "--columns", type=int, default=2, help="Number of columns per page."
    )
    parser.add_argument("--rows", type=int, default=3, help="Number of rows per page.")
    parser.add_argument(
        "--reading-order",
        type=str,
        choices=["right-to-left", "left-to-right"],
        default="right-to-left",
        help="Reading order: 'right-to-left' for manga, 'left-to-right' for western comics.",
    )
    parser.add_argument(
        "--split",
        type=str,
        choices=["fixed-size", "cut-space"],
        default="fixed-size",
        help="split mode: 'fixed-size' , 'cut-space' ",
    )
    parser.add_argument(
        "--temp-dir",
        type=Path,
        default=None,
        help="Temporary directory for intermediate files.",
    )

    args = parser.parse_args()

    convert_webtoon_to_comic(
        input_folder=args.input,
        output_file=args.output,
        temp_dir=args.temp_dir,
        panel_height=args.panel_height,
        page_width=args.page_width,
        page_height=args.page_height,
        columns=args.columns,
        rows=args.rows,
        reading_order=args.reading_order,
        split=args.split,
    )
