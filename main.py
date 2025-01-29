# Photomosaic is a program that takes an image and creates a mosaic of that image using smaller images.

import argparse
import os
from PIL import Image
from classes.photomosaic import Photomosaic


def main():
    parser = argparse.ArgumentParser(description="Create a photomosaic from an image.")
    parser.add_argument(
        "image", type=str, help="The image to create a photomosaic from."
    )
    parser.add_argument("project", type=str, help="The project name.")
    parser.add_argument(
        "--tile-size", type=int, default=50, help="The size of the tiles to use."
    )
    parser.add_argument(
        "--output", type=str, default="output.jpg", help="The output file name."
    )
    args = parser.parse_args()

    main_folder = f"project_{args.project}"

    # Check if project directory exists
    if not os.path.isdir(main_folder):
        raise FileNotFoundError(f"The directory '{main_folder}' does not exist.")

    # Check if the image exists
    main_image_file = os.path.join(main_folder, args.image)
    if not os.path.isfile(main_image_file):
        raise FileNotFoundError(f"The file '{main_image_file}' does not exist.")

    tiles_folder = os.path.join(main_folder, "tiles")

    # Check if the tiles directory exists
    if not os.path.isdir(tiles_folder):
        raise FileNotFoundError(f"The directory '{tiles_folder}' does not exist.")

    # Load and resize the main image
    main_image = Image.open(main_image_file)
    main_image = main_image.resize(
        (
            (main_image.width // args.tile_size) * args.tile_size,
            (main_image.height // args.tile_size) * args.tile_size,
        )
    )
    main_image = main_image.convert("RGB")

    # Create photomosaic
    photomosaic = Photomosaic(tiles_folder)

    # Check if there are enough tiles to create the photomosaic
    if photomosaic.get_available_tiles_count() < (
        main_image.width // args.tile_size
    ) * (main_image.height // args.tile_size):
        print("Not enough tiles to create the photomosaic.")
        print(
            f"You are trying to generate a photomosaic that requires {(main_image.width // args.tile_size) * (main_image.height // args.tile_size)} tiles, but there are only {photomosaic.get_available_tiles_count()} tiles available."
        )
        print(
            "Please generate more tiles for this project, or change the configuration to use less tiles."
        )
        exit()

    photomosaic_image = photomosaic.create_photomosaic(
        main_image=main_image, tile_size=args.tile_size
    )

    # Save the photomosaic
    photomosaic_image.save(os.path.join(main_folder, args.output))

    # Open image using default image viewer
    photomosaic_image.show()


if __name__ == "__main__":
    main()
