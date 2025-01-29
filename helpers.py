import os
import numpy as np
import json
from PIL import Image
from skimage.color import rgb2lab


def get_average_color_lab(image: Image) -> np.ndarray:
    """
    Get the average color of an image in the LAB color space.

    :param image: The image to get the average color of.
    :return: The average color of the image in the LAB color space.
    """
    # Convert image to NumPy array and then to LAB color space
    np_image = np.array(image)
    lab_image = rgb2lab(np_image)
    # Calculate the average LAB color
    w, h, d = lab_image.shape
    numpy_avg = np.average(lab_image.reshape(w * h, d), axis=0)

    return numpy_avg


def load_existing_tiles(folder: str) -> dict:
    """
    Load the list of existing tiles from the output directory.

    :param folder: The output directory to load the existing tiles from.
    :return: A dictionary containing the existing tiles and their counts.
    """
    existing_tiles = {}

    for filename in os.listdir(folder):
        tile_hash = filename[:64]
        if tile_hash in existing_tiles:
            existing_tiles[tile_hash] += 1
        else:
            existing_tiles[tile_hash] = 1

    print(f"Loaded {len(existing_tiles)} existing tiles.")
    return existing_tiles


def load_lab_mapping(folder: str) -> dict:
    file_path = os.path.join(folder, "lab_mapping.json")

    if not os.path.exists(file_path):
        return {}

    # Load mapping from JSON file
    with open(file_path, "r") as lab_file:
        lab_mapping = json.load(lab_file)

    return lab_mapping
