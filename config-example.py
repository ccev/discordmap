from map.config import MAD, RDM, Area, Icons
EMOJIS = {}
ICONSET = None
# ^^^^ IGNORE ^^^^

DB_HOST = "0.0.0.0"
DB_PORT = 3306
DB_USER = ""
DB_PASSWORD = ""
DB_NAME = "mad"
DB_SCHEMA = MAD  # unused (only mad support)

MAP_WIDTH = 700
MAP_HEIGHT = 400
MAP_SCALE = 1
TILESERVER = "https://tiles.url.com/"
STYLES = [("OSM Bright", "osm-bright")]  # name, tileserver ID
MARKER_LIMIT = 100

ADMINS = [211562278800195584]  # unused rn
EMOJI_SERVER = 12345678912345678
TOKEN = ""

AREAS = [
    Area("Main", 30.132131, 12.0132121, 13),
    Area("Secondary", 31.12713, 12.98163, 15.5)
]
# The first listed area will be used on map start
# Format: Name, lat, lon, zoom

ICONSETS = [
    Icons("Pogo (outline)", "https://raw.githubusercontent.com/whitewillem/PogoAssets/main/uicons-outline/"),
    Icons("Pogo", "https://raw.githubusercontent.com/whitewillem/PogoAssets/main/uicons/"),
    # Icons("HOME (outline)", "https://raw.githubusercontent.com/nileplumb/PkmnHomeIcons/master/UICONS_OS_128/"),
    # Icons("HOME", "https://raw.githubusercontent.com/nileplumb/PkmnHomeIcons/master/UICONS/"),
    # Icons("Shuffle", "https://raw.githubusercontent.com/nileplumb/PkmnShuffleMap/master/UICONS/")
]
# The first listed Iconset will be used on map start. Only UICONS are supported
# Format: Name, URL
# Note that currently only the 2 willem iconsets are supported, so the otheres are commented out
