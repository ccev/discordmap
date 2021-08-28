from __future__ import annotations
from typing import TYPE_CHECKING
import discord
from config import EMOJIS
from map.settings import Settings

if TYPE_CHECKING:
    from map.map import Map

DEFAULT_ROW = 2


def get_emoji(name):
    return EMOJIS.get(name, "❓")


class BaseMapControlButton(discord.ui.Button):
    def __init__(self, dmap: Map, label: str, row: int = DEFAULT_ROW):
        emoji = get_emoji(label)
        super().__init__(style=discord.ButtonStyle.grey, emoji=emoji, row=row)
        self.dmap = dmap

    async def _callback(self, interaction: discord.Interaction):
        await interaction.response.defer()
        if not self.dmap.is_author(interaction.user.id):
            return
        await self.dmap.start_load()
        await self.dmap.update()


class EmptyButton(discord.ui.Button):
    def __init__(self, custom_id: int):
        super().__init__(style=discord.ButtonStyle.grey, emoji=get_emoji("mapBl"), disabled=True,
                         custom_id=str(custom_id), row=DEFAULT_ROW)


class MultiplierButton(discord.ui.Button):
    def __init__(self, dmap: Map):
        self.multipliers = [1, 0.5, 3, 2]
        super().__init__(style=discord.ButtonStyle.green, label=str(self.multipliers[0]) + "x", custom_id="multiplier",
                         row=DEFAULT_ROW)
        self.dmap = dmap

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer()
        if not self.dmap.is_author(interaction.user.id):
            return
        multiplier = self.multipliers.pop()
        self.multipliers.insert(0, multiplier)
        self.dmap.multiplier = multiplier
        self.label = str(multiplier) + "x"
        await self.dmap.edit()


class SettingsButton(discord.ui.Button):
    def __init__(self, dmap: Map):
        super().__init__(style=discord.ButtonStyle.blurple, label="Settings", row=DEFAULT_ROW + 1)
        self.dmap = dmap

    async def callback(self, interaction: discord.Interaction):
        settings = Settings(self.dmap)
        await settings.send(interaction.response)


class UpButton(BaseMapControlButton):
    def __init__(self, dmap: Map):
        super().__init__(dmap, "mapUp")

    async def callback(self, interaction: discord.Interaction):
        self.dmap.lat += self.dmap.get_lat_offset()
        await self._callback(interaction)


class LeftButton(BaseMapControlButton):
    def __init__(self, dmap: Map):
        super().__init__(dmap, "mapLe", 3)

    async def callback(self, interaction: discord.Interaction):
        self.dmap.lon -= self.dmap.get_lon_offset()
        await self._callback(interaction)


class DownButton(BaseMapControlButton):
    def __init__(self, dmap: Map):
        super().__init__(dmap, "mapDo", 3)

    async def callback(self, interaction: discord.Interaction):
        self.dmap.lat -= self.dmap.get_lat_offset()
        await self._callback(interaction)


class RightButton(BaseMapControlButton):
    def __init__(self, dmap: Map):
        super().__init__(dmap, "mapRi", 3)

    async def callback(self, interaction: discord.Interaction):
        self.dmap.lon += self.dmap.get_lon_offset()
        await self._callback(interaction)


class ZoomInButton(BaseMapControlButton):
    def __init__(self, dmap: Map):
        super().__init__(dmap, "mapPl")

    async def callback(self, interaction: discord.Interaction):
        self.dmap.zoom += 0.25 * self.dmap.multiplier
        await self._callback(interaction)


class ZoomOutButton(BaseMapControlButton):
    def __init__(self, dmap: Map):
        super().__init__(dmap, "mapMi", 3)

    async def callback(self, interaction: discord.Interaction):
        self.dmap.zoom -= 0.25 * self.dmap.multiplier
        await self._callback(interaction)
