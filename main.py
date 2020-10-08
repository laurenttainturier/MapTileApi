from os import makedirs, path
from PIL import Image
import math


def save_image(image: Image):
    image.save('crop_0_0.jpg')


class LatLng:
    def __init__(self, lat, lng):
        self.lat = lat
        self.lng = lng


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return f"x: {self.x}, y: {self.y}"


class TileCoord(Point):
    def __init__(self, x: float, y: float, z: int):
        super().__init__(round(x), round(y))
        self.zoom = z

    def __str__(self):
        return f"x: {self.x}, y: {self.y}, z: {self.zoom}"


def fromLatLngToPoint(latlng: LatLng, tile_size: int) -> Point:
    mercator = - math.log(math.tan((0.25 + latlng.lat / 360) * math.pi))
    return Point(
        tile_size * (latlng.lng / 360 + 0.5),
        tile_size / 2 * (1 + mercator / math.pi))


def fromLatLngToTileCoord(latlng: LatLng, zoom: int, tile_size: int) -> TileCoord:
    point = fromLatLngToPoint(latlng, tile_size)
    scale = 2 ** zoom

    return TileCoord(
        point.x * scale,
        point.y * scale,
        zoom
    )


def save_zoom(image: Image, zoom, x, y, root_directory='./images'):
    directory = path.join(root_directory, str(zoom), str(x))
    makedirs(directory, exist_ok=True)
    image.save(path.join(directory, f"{y}.png"), 'PNG')


if __name__ == "__main__":
    TILE_SIZE = 128
    IMAGE_PATH = 'images/image.jpg'

    tile_size = TILE_SIZE
    image = Image.open(IMAGE_PATH)
    image_width, image_height = image.size

    latlng0 = LatLng(48.848364, 2.30271)
    latlng1 = LatLng(48.819998, 2.345894)
    image_is_too_small = False

    for zoom in range(19, 20):
        if image_is_too_small:
            tile_size //= 2

        print(f"Generating images for zoom level {zoom} with a tile size of {tile_size}px")
        top_left_pixel = fromLatLngToTileCoord(latlng0, zoom, tile_size)
        bottom_right_pixel = fromLatLngToTileCoord(latlng1, zoom, tile_size)
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
                img_tile.paste(cropImg.crop(coords), (tx_0 if px0 == 0 else 0, ty_0 if py0 == 0 else 0))
                save_zoom(img_tile, zoom, i + tile0_l, j + tile0_c)
