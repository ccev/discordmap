from __future__ import annotations
from typing import List, Dict, Any, Optional, TYPE_CHECKING
import config

if TYPE_CHECKING:
    from map.map import Map


class MapObject:
    id: str
    lat: float
    lon: float
    url: str
    size: int = 0
    height: Optional[int] = None
    width: Optional[int] = None
    y_offset: int = 0
    x_offset: int = 0
    uicon_category: str

    def get_markers(self) -> List[Dict[str, Any]]:
        if not self.height:
            self.height = self.size
        if not self.width:
            self.width = self.size
        return [{
            "url": self.url,
            "latitude": self.lat,
            "longitude": self.lon,
            "width": self.width,
            "height": self.height,
            "x_offset": self.x_offset,
            "y_offset": self.y_offset
        }]


class Pokemon(MapObject):
    uicon_category = "pokemon"

    def __init__(self, data: tuple, dmap: Map):
        self.lat, self.lon, mon_id, form, costume = data
        uicon = str(mon_id)
        if form:
            uicon += f"_f{form}"
        if costume:
            uicon += f"_c{costume}"
        self.url = config.ICONSET.url.format(f"{self.uicon_category}/{uicon}")
        self.size = dmap.get_marker_size(15)


class Gym(MapObject):
    uicon_category = "gym"

    def __init__(self, data: tuple, dmap: Map):
        self.lat, self.lon, team_id, level = data
        uicon = str(team_id)
        if team_id and level:
            uicon += f"_t{level}"

        self.url = config.ICONSET.url.format(f"{self.uicon_category}/{uicon}")
        self.size = dmap.get_marker_size()
        self.y_offset = self.size // -2


class Pokestop(MapObject):
    uicon_category = "pokestop"

    def __init__(self, data: tuple, dmap: Map):
        self.lat, self.lon = data
        self.url = config.ICONSET.url.format(f"{self.uicon_category}/0")
        self.size = dmap.get_marker_size(17)
        self.y_offset = self.size // -2


class Grunt(MapObject):
    uicon_category = "invasion"

    def __init__(self, data: tuple, dmap: Map):
        self.lat, self.lon, grunt_id = data
        self.stop = Pokestop((self.lat, self.lon), dmap)
        self.stop.url.replace(".png", "_i.png")
        self.url = config.ICONSET.url.format(f"{self.uicon_category}/{grunt_id}")

        self.y_offset = - dmap.get_marker_size(10)
        self.x_offset = dmap.get_marker_size(5)
        self.size = dmap.get_marker_size(13)

    def get_markers(self) -> List[Dict[str, Any]]:
        markers = []
        markers += self.stop.get_markers()
        markers += super().get_markers()
        return markers


class _RaidEgg(MapObject):
    uicon_category = "raid/egg"

    def __init__(self, data: tuple, dmap: Map):
        self.lat, self.lon, level = data
        self.url = config.ICONSET.url.format(f"{self.uicon_category}/{level}")
        self.size = dmap.get_marker_size()


class Raid(MapObject):
    uicon_category = ""

    def __init__(self, data: tuple, dmap: Map):
        self.lat, self.lon, team, mon_id, form, costume, raid_level = data
        self.gym = Gym((self.lat, self.lon, team, 0), dmap)

        if mon_id:
            self.boss = Pokemon((self.lat, self.lon, mon_id, form, costume), dmap)
        else:
            self.boss = _RaidEgg((self.lat, self.lon, raid_level), dmap)
        self.boss.y_offset = - dmap.get_marker_size(12)
        self.boss.x_offset = - dmap.get_marker_size(3)
        self.boss.size = dmap.get_marker_size(15)

    def get_markers(self) -> List[Dict[str, Any]]:
        markers = []
        markers += self.gym.get_markers()
        markers += self.boss.get_markers()
        return markers
