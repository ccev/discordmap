from map.config import Schema, Area
EMOJIS = {}
# ^^^^ IGNORE ^^^^

DB_HOST = "0.0.0.0"
DB_PORT = 3306
DB_USER = ""
DB_PASSWORD = ""
DB_NAME = "mad"
DB_SCHEMA = Schema.MAD  # unused (only mad support)

MAP_WIDTH = 700
MAP_HEIGHT = 400
MAP_SCALE = 1
TILESERVER = "https://tiles.url.com/"
STYLES = [("OSM Bright", "osm-bright")]  # name, tileserver ID

ADMINS = [211562278800195584]  # unused rn
EMOJI_SERVER = 12345678912345678
TOKEN = ""

AREAS = [
    Area("Main", 30.132131, 12.0132121, 13),
    Area("Secondary", 31.12713, 12.98163, 15.5)
]
# The first listed area will be used on map start
# Format: Name, lat, lon, zoom
