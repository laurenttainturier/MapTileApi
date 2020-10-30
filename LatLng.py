import math
from typing import Tuple

from tilecoord import TileCoord


class LatLng:
    """
    This class represents the coordinate of a point on earth based on
    its latitude and longitude
    """

    def __init__(self, lat, lng):
        self.lat = lat
        self.lng = lng

    def convert_to_point(self, tile_size) -> Tuple[float, float]:
        mercator = - math.log(math.tan((0.25 + self.lat / 360) * math.pi))
        return tile_size * (self.lng / 360 + 0.5), tile_size / 2 * (1 + mercator / math.pi)

    def convert_to_tile_coord(self, tile_size: int, zoom: int) -> TileCoord:
        """
        Return the coordinates in pixels of point for a given tile size and level of zoom
        :param tile_size: tile size in pixels
        :param zoom: level of zoom
        :return: Coordinate of the point in pixels
        """
        x, y = self.convert_to_point(tile_size)
        scale = 2 ** zoom

        return TileCoord(x * scale, y * scale, zoom)
