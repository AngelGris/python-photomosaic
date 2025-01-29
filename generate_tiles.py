# Process images to generate tiles used in the photomosaic.

import argparse
import os
import hashlib
import json
from PIL import Image
from helpers import get_average_color_lab, load_existing_tiles, load_lab_mapping


def main():
    parser = argparse.ArgumentParser(
        description="Process images to generate tiles used in the photomosaic."
    )
    parser.add_argument(
        "project",
        type=str,
        help="The project you are working on.",
    )
    args = parser.parse_args()

    main_folder = f"project_{args.project}"
    input_folder = os.path.join(main_folder, "input")
    output_folder = os.path.join(main_folder, "tiles")
    processed_folder = os.path.join(main_folder, "processed")

    # Check if the input directory exists
    if not os.path.isdir(input_folder):
        raise FileNotFoundError(f'The directory "{input_folder}" does not exist.')

    # Create the output directory if it does not exist
    if os.path.exists(output_folder):
        # Request user confirmation to overwrite the output directory
        response = input(
            f'The directory "{output_folder}" already exists. Do you want to add new images to it? (This could generate duplicated tiles) (y/n)'
        )
        if response.lower() != "y":
            print("Exiting...")
            exit()
    else:
        os.makedirs(output_folder)

    # Create the processed directory if it does not exist
    if not os.path.exists(processed_folder):
        os.makedirs(processed_folder)

    # Load list of existing files in output folder
    existing_tiles = load_existing_tiles(output_folder)
    lab_mapping = load_lab_mapping(output_folder)

    # Loop through all jpg files in the input directory
    for filename in os.listdir(input_folder):
        if filename.endswith(".jpg"):
            # Load the image
            image = Image.open(os.path.join(input_folder, filename))
            image = image.convert("RGB")

            image_lab = get_average_color_lab(image)
            tile_name_hash = f"l{image_lab[0]}a{image_lab[1]}b{image_lab[2]}".encode(
                "utf-8"
            )
            tile_name_hash = hashlib.sha256(tile_name_hash).hexdigest()

            if tile_name_hash in existing_tiles:
                existing_tiles[tile_name_hash] += 1
            else:
                existing_tiles[tile_name_hash] = 1

            if tile_name_hash not in lab_mapping:
                lab_mapping[tile_name_hash] = image_lab.tolist()

            tile_filename = f"{tile_name_hash}_{existing_tiles[tile_name_hash]}.jpg"

            # Crop central square of the image
            width, height = image.size
            if width > height:
                left = (width - height) // 2
                right = left + height
                top = 0
                bottom = height
            else:
                top = (height - width) // 2
                bottom = top + width
                left = 0
                right = width

            image = image.crop((left, top, right, bottom))

            # Save the image
            image.save(os.path.join(output_folder, tile_filename))

            # Move processed image to processed folder
            os.rename(
                os.path.join(input_folder, filename),
                os.path.join(processed_folder, filename),
            )

    # Save the lab mapping as JSON
    with open(os.path.join(output_folder, "lab_mapping.json"), "w") as lab_file:
        json.dump({k: v for k, v in lab_mapping.items()}, lab_file, indent=4)


if __name__ == "__main__":
    main()
