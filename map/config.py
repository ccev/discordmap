from enum import Enum
from typing import Tuple


class Schema(Enum):
    MAD = 1
    RDM = 2


class Area:
    name: str
    lat: float
    lon: float
    zoom: float

    def __init__(self, name: str, lat: float, lon: float, zoom: float):
        self.name = name
        self.lat = lat
        self.lon = lon
        self.zoom = zoom


class Icons:
    name: str
    url: str

    def __init__(self, name: str, url: str):
        self.name = name
        self.url = url + "{}.png"
