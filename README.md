# Python Photomosaic Generator

This is a simple photomosaic generator written in Python. It takes an input image and a folder of images to use as tiles
and generates a photomosaic from the input image.

## Installation

To install the required packages, run the following command:

```bash
pip install -r requirements.txt
```

## Usage

### Generating the tiles

In order to be able to generate a photomosaic, you first need to generate the tiles.
To do this create a folder with the name `project_{your project name}`, i.e. `project_myproject`. Inside this folder
create a folder called `input` and place all the images you want to use as tiles in this folder.

---
**NOTE**

For now the input images can only be `.jpg` files. Support for PNG will be added in the future.

---

Then run the following command:

```bash
python generate_tiles.py {your project name}
```

This will process all the images in the `input` folder and save the tiles in the `tiles` folder.

To generate the tiles it just cuts out the center square of each image, and processed images are moved to the
`processed` folder.

At the end of the process the `input` folder should be empty, `processed` should contain all the original images, and
`tiles` should contain all the tiles and a `lab_mapping.json` file.

If there's an error while processing the images, you might need to fix the problem (i.e. an error with an image) and
restart the process. To restart the process moved all the processed images back to the `input` folder, delete the
`tiles` folder and all its contents, and run the command again.

If after generating tiles you want to add extra tiles to the collection, just add the images to the `input` folder and
run the command again. You'll get a confirmation message because if you are processing again images you already
processed, then you'll have duplicated tiles.

### Generating the photomosaic

To generate the photomosaic using the generated tiles, place the image you want to generate in the project folder and
run the following command:

```bash
python main.py {image} {project} --tile-size={tile size} --output={output file}
```

Where:

* **{image}** is the file name of the image you want to generate the photomosaic from.
* **{project}** is the name of the project you used to generate the tiles.
* **{tile size}** [optional] is the size of the tiles you want to use. Default is 50.
* **{output file}** [optional] is the name of the file you want to save the photomosaic to. Default is 'output.jpg'.


This will generate the photomosaic and save it to the main folder.

---
**NOTE**

* The more tiles you have, the better the photomosaic will look. The tiles should be as varied as possible to get the best.
* The main image should be big enough and don't have too much detail, otherwise the photomosaic will not look good.

---

## Further improvements

- Add support for PNG images as input, but save all tiles as JPG for performance.
- Add support for different output image width and/or height (--output-width and --output-height).