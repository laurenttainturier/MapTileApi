from os import makedirs, path
from PIL import Image

from latlng import LatLng


def save_zoom(image_to_save: Image, zoom_level, x, y, root_directory='./images'):
    directory = path.join(root_directory, str(zoom_level), str(x))
    makedirs(directory, exist_ok=True)
    image_to_save.save(path.join(directory, f"{y}.png"), 'PNG')


class MapImage:
    def __init__(self, top: int, left: int, bottom: int, right: int, tile_size: int):
        self.top = top
        self.left = left
        self.bottom = bottom
        self.right = right
        self.tile_size = tile_size

        self.min_horizontal_tile = self.left // self.tile_size
        self.max_horizontal_tile = self.right // self.tile_size

        self.min_vertical_tile = self.top // self.tile_size
        self.max_vertical_tile = self.bottom // self.tile_size

    def crop_image(self):
        pass


if __name__ == "__main__":
    TILE_SIZE = 128
    IMAGE_PATH = 'images/image.jpg'

    tile_size = TILE_SIZE
    image = Image.open(IMAGE_PATH)
    image_width, image_height = image.size

    north_west_latlng = LatLng(48.848364, 2.30271)
    south_east_latlng = LatLng(48.819998, 2.345894)
    image_is_too_small = False

    for zoom in range(19, 20):
        if image_is_too_small:
            tile_size //= 2

        print(f"Generating images for zoom level {zoom} with a tile size of {tile_size}px")
        top_left_pixel = north_west_latlng.convert_to_tile_coord(zoom, tile_size)
        bottom_right_pixel = south_east_latlng.convert_to_tile_coord(zoom, tile_size)
        width = bottom_right_pixel.x - top_left_pixel.x
        height = bottom_right_pixel.y - top_left_pixel.y

        cropImg = Image.new('RGBA', image.size, (255, 255, 255, 0))
        cropImg.paste(image, (0, 0))
        if width > image_width or height > image_height:
            cropImg = cropImg.resize((width, height))
            image_is_too_small = True
        else:
            cropImg.thumbnail((width, height), Image.ANTIALIAS)

        tile0_l = top_left_pixel.x // tile_size
        tile0_c = top_left_pixel.y // tile_size

        tile1_l = bottom_right_pixel.x // tile_size
        tile1_c = bottom_right_pixel.y // tile_size

        tx_0 = top_left_pixel.x - tile0_l * tile_size
        ty_0 = top_left_pixel.y - tile0_c * tile_size

        img_tile_template = Image.new('RGBA', (tile_size, tile_size), (255, 255, 255, 0))
        for i in range(0, tile1_l - tile0_l + 1):
            for j in range(0, tile1_c - tile0_c + 1):
                px0 = max(i * tile_size - tx_0, 0)
                py0 = max(j * tile_size - ty_0, 0)
                coords = (px0, py0, px0 + tile_size, py0 + tile_size)

                img_tile = img_tile_template.copy()
                img_tile.paste(
                    cropImg.crop(coords),
                    (tx_0 if px0 == 0 else 0, ty_0 if py0 == 0 else 0))
                save_zoom(img_tile, zoom, i + tile0_l, j + tile0_c)
