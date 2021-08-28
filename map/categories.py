from __future__ import annotations
import discord
import aiomysql
from typing import TYPE_CHECKING, List, Type

from map.map_objects import MapObject, Pokemon, Gym, Raid, Pokestop, Grunt
from config import DB_HOST, DB_NAME, DB_PORT, DB_USER, DB_SCHEMA, DB_PASSWORD
from map.buttons import get_emoji

if TYPE_CHECKING:
    from map.map import Map


class Category(discord.SelectOption):
    name: str
    emoji: str
    map_object: MapObject
    query: str
    dmap: Map

    def __init__(self, i: int, dmap: Map):
        emoji = get_emoji(self.emoji)
        super().__init__(label=self.name,
                         value=str(i),
                         description=f"Display {self.name} on the map",
                         emoji=emoji)
        self.dmap = dmap

    @staticmethod
    async def fetch(query, bbox):
        if "where" in query.lower():
            query += " and"
        else:
            query += " where"
        query += " latitude > {} and latitude < {} " \
                 "and longitude > {} and longitude < {}".format(bbox[0], bbox[2], bbox[1], bbox[3])
        conn = await aiomysql.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASSWORD,
            db=DB_NAME)
        async with conn.cursor() as cursor:
            await cursor.execute(query)
            r = await cursor.fetchall()
        conn.close()
        return r

    async def get_map_objects(self, bbox) -> List[MapObject]:
        objects = []
        result = await self.fetch(self.query, bbox)
        for data in result:
            map_object = self.map_object(data, self.dmap)
            objects.append(map_object)
        return objects


class PokemonCategory(Category):
    name = "Pokémon"
    emoji = "mapPo"
    query = ("select latitude, longitude, pokemon_id, form, costume "
             "from pokemon "
             "where disappear_time > utc_timestamp()")
    map_object = Pokemon


class RaidCategory(Category):
    name = "Raids"
    emoji = "mapRa"
    query = ("select latitude, longitude, team_id, pokemon_id, raid.form, raid.costume, raid.level "
             "from raid left join gym on raid.gym_id = gym.gym_id "
             "where end > utc_timestamp()")
    map_object = Raid


class PokestopCategory(Category):
    name = "Pokéstops"
    emoji = "mapSt"
    query = "select latitude, longitude from pokestop"
    map_object = Pokestop


class GymCategory(Category):
    name = "Gyms"
    emoji = "mapGy"
    query = ("select latitude, longitude, team_id, (6 - slots_available)" 
             "from gym")
    map_object = Gym


class QuestCategory(Category):
    name = "Quests"
    emoji = "mapQu"
    query = "select latitude, longitude from pokestop"
    map_object = Pokestop


class GruntCategory(Category):
    name = "Grunts"
    emoji = "mapGr"
    query = ("select latitude, longitude, incident_grunt_type "
             "from pokestop "
             "where incident_expiration > utc_timestamp()")
    map_object = Grunt


class CategorySelect(discord.ui.Select):
    def __init__(self, dmap: Map):
        super().__init__(custom_id="categories", placeholder="Choose a category to display", min_values=0)
        self.categories = []
        for i, category in enumerate([PokemonCategory, RaidCategory, GymCategory,
                                      PokestopCategory, QuestCategory, GruntCategory]):
            fin_cat = category(i, dmap)
            self.categories.append(fin_cat)
            self.options.append(fin_cat)
        self.max_values = len(self.options)

        self.dmap = dmap

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer()
        if not self.dmap.is_author(interaction.user.id):
            return
        await self.dmap.start_load()

        values = list(map(int, self.values))
        for i, option in enumerate(self.options):
            option.default = bool(i in values)

        await self.dmap.update()
