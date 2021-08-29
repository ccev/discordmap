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

    def make_uicon(self, *args):
        combinations = []
        args = list(map(str, args))
        for i in range(1, len(args) + 1):
            combinations.insert(0, args[:i])
        i = 0
        for combination in combinations.copy():
            if len(combination) > 2:
                new_combination = combination.copy()
                del new_combination[-2]
                combinations.insert(i + 2, new_combination)
                i += 2
        combinations.append(["0"])

        for combination in combinations:
            name = "_".join(combination) + ".png"
            if name in config.ICONSET.index.get(self.uicon_category, []):
                self.url = config.ICONSET.url + f"{self.uicon_category}/{name}"
                return
        self.url = config.ICONSET.url + "pokemon/0.png"


class Pokemon(MapObject):
    uicon_category = "pokemon"

    def __init__(self, data: tuple, dmap: Map):
        self.lat, self.lon, mon_id, form, costume = data
        self.make_uicon(mon_id, f"f{form}", f"c{costume}")
        self.size = dmap.get_marker_size(15)


class Gym(MapObject):
    uicon_category = "gym"

    def __init__(self, data: tuple, dmap: Map):
        self.lat, self.lon, team_id, level = data
        self.make_uicon(team_id, f"t{level}")

        self.size = dmap.get_marker_size()
        self.y_offset = self.size // -2


class Pokestop(MapObject):
    uicon_category = "pokestop"

    def __init__(self, data: tuple, dmap: Map, *uicon_args):
        self.lat, self.lon = data
        self.make_uicon(0, *uicon_args)
        self.size = dmap.get_marker_size(17)
        self.y_offset = self.size // -2


class Grunt(MapObject):
    uicon_category = "invasion"

    def __init__(self, data: tuple, dmap: Map):
        self.lat, self.lon, grunt_id = data
        self.stop = Pokestop((self.lat, self.lon), dmap, "i")
        self.make_uicon(grunt_id)

        self.y_offset = - dmap.get_marker_size(10)
        self.x_offset = dmap.get_marker_size(-5)
        self.size = dmap.get_marker_size(13)

    def get_markers(self) -> List[Dict[str, Any]]:
        markers = []
        markers += self.stop.get_markers()
        markers += super().get_markers()
        return markers


class RaidEgg(MapObject):
    uicon_category = "raid/egg"

    def __init__(self, data: tuple, dmap: Map):
        self.lat, self.lon, level = data
        self.make_uicon(level)
        self.size = dmap.get_marker_size()


class Raid(MapObject):
    def __init__(self, data: tuple, dmap: Map):
        self.lat, self.lon, team, mon_id, form, costume, raid_level = data
        self.gym = Gym((self.lat, self.lon, team, 0), dmap)

        if mon_id:
            self.boss = Pokemon((self.lat, self.lon, mon_id, form, costume), dmap)
        else:
            self.boss = RaidEgg((self.lat, self.lon, raid_level), dmap)
        self.boss.y_offset = - dmap.get_marker_size(12)
        self.boss.x_offset = - dmap.get_marker_size(3)
        self.boss.size = dmap.get_marker_size(15)

    def get_markers(self) -> List[Dict[str, Any]]:
        markers = []
        markers += self.gym.get_markers()
        markers += self.boss.get_markers()
        return markers
