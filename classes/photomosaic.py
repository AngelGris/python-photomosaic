# Description: This file contains the Photomosaic class which is used to create a photomosaic from an image
# using a list of tiles.

import numpy as np
from PIL import Image
from helpers import get_average_color_lab, load_existing_tiles, load_lab_mapping
from classes.tracer import Tracer


class Photomosaic:
    def __init__(self, tiles_folder: str):
        self._tiles_folder = tiles_folder
        self.tiles_used = {}
        self._available_tiles = load_existing_tiles(self._tiles_folder)
        self._lab_mapping = load_lab_mapping(self._tiles_folder)
        self._tracer = Tracer()

    def _get_best_tile(self, tile_color: np.ndarray) -> str:
        """
        Get the best tile to use for a section of the main image.

        :param color: The average LAB color of the section.
        :param available_tiles: The available tiles to choose from.
        :return: The best tile to use for the section.
        """
        best_tile = None
        best_distance = float("inf")

        for tile, color in self._lab_mapping.items():
            if (
                tile in self.tiles_used
                and self.tiles_used[tile] >= self._available_tiles[tile]
            ):
                continue

            distance = np.linalg.norm(tile_color - color)
            if distance < best_distance:
                best_tile = tile
                best_distance = distance

        if best_tile not in self.tiles_used:
            self.tiles_used[best_tile] = 0

        self.tiles_used[best_tile] += 1

        return best_tile

    def get_available_tiles_count(self):
        return len(self._available_tiles)

    def _merge_tile(
        self, mosaic_image: Image, tile: str, tile_size: int, x: int, y: int
    ) -> Image:
        """
        Merge a tile into the photomosaic image.

        :param mosaic_image: The photomosaic image to merge the tile into.
        :param tile: The tile filename to merge into the photomosaic image.
        :param tile_size: The size of the tiles.
        :param x: The x-coordinate to place the tile at.
        :param y: The y-coordinate to place the tile at.
        :return: The photomosaic image with the tile merged into it.
        """
        tile = Image.open(f"{self._tiles_folder}/{tile}_1.jpg")
        tile = tile.resize((tile_size, tile_size))
        mosaic_image.paste(tile, (x, y))
        return

    def create_photomosaic(self, main_image: Image, tile_size: int) -> Image:
        """
        Create a photomosaic from an image using a list of tiles.

        :param main_image: The image to create a photomosaic from.
        :param tile_size: The size of the tiles to use.
        :return: The photomosaic created from the image.
        """
        self._tracer.start_tracing("create_photomosaic")
        self.tiles_used = {}

        mosaic_image = Image.new("RGB", main_image.size)
        total_tiles = 0
        for i in range(0, main_image.width, tile_size):
            for j in range(0, main_image.height, tile_size):
                section = main_image.crop((i, j, i + tile_size, j + tile_size))
                section_color = get_average_color_lab(section)
                tile = self._get_best_tile(section_color)
                self._merge_tile(
                    mosaic_image=mosaic_image, tile=tile, tile_size=tile_size, x=i, y=j
                )
                total_tiles += 1

        total_time = self._tracer.stop_tracing(
            "create_photomosaic",
            f"Photomosaic with {total_tiles} tiles created in {{:.2f}} seconds.",
        )
        print(f"{total_tiles / total_time:.2f} tiles per second.")
        return mosaic_image
