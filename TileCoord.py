class TileCoord:
    """
    This class is used to represent the coordinates and
    level of zoom of a map tile
    """

    def __init__(self, x: int, y: int, zoom: int):
        self.x = x
        self.y = y
        self.zoom = zoom
