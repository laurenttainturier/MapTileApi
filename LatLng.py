import math
from typing import Tuple

from TileCoord import TileCoord


class LatLng:
    def __init__(self, lat, lng):
        self.lat = lat
        self.lng = lng

    def convertToPoint(self, tile_size) -> Tuple[float, float]:
        mercator = - math.log(math.tan((0.25 + self.lat / 360) * math.pi))
        return tile_size * (self.lng / 360 + 0.5), tile_size / 2 * (1 + mercator / math.pi)

    def convertToTileCoord(self, tile_size: int, zoom: int) -> TileCoord:
        x, y = self.convertToPoint(tile_size)
        scale = 2 ** zoom

        return TileCoord(x * scale, y * scale, zoom)
