from PIL import Image
import numpy as np
import os


def detect_cut_positions(image, threshold_ratio=0.1, min_consecutive=10):
    """
    檢測 Webtoon 圖片中的切割位置。
    """
    image = image.convert("RGB")
    image_array = np.array(image)
    height, width, _ = image_array.shape
    threshold_width = int(threshold_ratio * width)

    cut_positions = []
    consecutive_count = 0
    start_cut = None

    for y in range(height):
        row = image_array[y, :, :]
        std_dev = np.std(row, axis=0)
        gradient = np.max(row, axis=0) - np.min(row, axis=0)

        mean_color = np.mean(row, axis=0)
        color_deviation = np.sqrt(np.sum((row - mean_color) ** 2, axis=1))
        non_main_color_pixels = np.sum(color_deviation > 10)

        if (
            np.all(std_dev < 5)
            and np.all(gradient < 10)
            and non_main_color_pixels < threshold_width
        ):
            if start_cut is None:
                start_cut = y
            consecutive_count += 1
        else:
            if consecutive_count >= min_consecutive:
                cut_positions.append((start_cut, y))
            start_cut = None
            consecutive_count = 0

    return cut_positions


def remove_top_margins(image, min_consecutive=10, threshold_ratio=0.1):
    """
    移除圖片上方的單色或漸層區塊。
    """
    image_array = np.array(image)
    height, width, _ = image_array.shape
    threshold_width = int(threshold_ratio * width)
    start_cut = 0
    consecutive_count = 0

    for y in range(height):
        row = image_array[y, :, :]
        std_dev = np.std(row, axis=0)
        gradient = np.max(row, axis=0) - np.min(row, axis=0)

        mean_color = np.mean(row, axis=0)
        color_deviation = np.sqrt(np.sum((row - mean_color) ** 2, axis=1))
        non_main_color_pixels = np.sum(color_deviation > 10)

        if (
            np.all(std_dev < 5)
            and np.all(gradient < 10)
            and non_main_color_pixels < threshold_width
        ):
            consecutive_count += 1
            if consecutive_count >= min_consecutive:
                start_cut = y
        else:
            if consecutive_count >= min_consecutive:
                break
            consecutive_count = 0

    return Image.fromarray(image_array[start_cut:, :, :])


def split_webtoon_image(image):
    image = image.convert("RGB")
    image_array = np.array(image)

    cut_positions = detect_cut_positions(image)

    prev_cut = 0
    index = 1
    ilist = []
    for start, end in cut_positions:
        if prev_cut < start:
            sub_image = image_array[prev_cut:start, :, :]
            sub_image = Image.fromarray(sub_image)
            if index == 1:
                sub_image = remove_top_margins(sub_image)
            ilist.append(sub_image)
            index += 1
        prev_cut = end
    return ilist
