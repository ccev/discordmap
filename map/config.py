class RDM:
    bbox_filter = " lat > {} and lat < {} and lon > {} and lon < {}"
    pokemon = ("select lat, lon, pokemon_id, form, costume "
               "from pokemon "
               "where expire_timestamp > curtime()")
    raids = ("select lat, lon, team_id, raid_pokemon_id, raid_pokemon_form, raid_pokemon_costume, raid_level "
             "from raid "
             "where raid_end_timestamp > curtime()")
    stops = "select lat, lon from pokestop"
    gyms = ("select lat, lon, team_id, (6 - available_slots)" 
            "from gym")
    quests = "select lat, lon from pokestop"
    grunts = ("select lat, lon, grunt_type "
              "from pokestop "
              "where incident_expire_timestamp > curtime()")


class MAD:
    bbox_filter = " latitude > {} and latitude < {} and longitude > {} and longitude < {}"
    pokemon = ("select latitude, longitude, pokemon_id, form, costume "
               "from pokemon "
               "where disappear_time > utc_timestamp()")
    raids = ("select latitude, longitude, team_id, pokemon_id, raid.form, raid.costume, raid.level "
             "from raid left join gym on raid.gym_id = gym.gym_id "
             "where end > utc_timestamp()")
    stops = "select latitude, longitude from pokestop"
    gyms = ("select latitude, longitude, team_id, (6 - slots_available)" 
            "from gym")
    quests = "select latitude, longitude from pokestop"
    grunts = ("select latitude, longitude, incident_grunt_type "
              "from pokestop "
              "where incident_expiration > utc_timestamp()")


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
