from __future__ import annotations
from typing import TYPE_CHECKING
import discord
from config import STYLES

if TYPE_CHECKING:
    from map.map import Map


class StyleSelect(discord.ui.Select):
    def __init__(self, dmap: Map):
        super().__init__(custom_id="styleselect",
                         placeholder="Choose a map style",
                         min_values=0,
                         max_values=1,
                         row=0)
        for i, (style_name, style_value) in enumerate(STYLES):
            style_name = "Map Style: " + style_name
            self.options.append(discord.SelectOption(label=style_name, value=style_value, default=i == 0))
        self.dmap = dmap

    async def callback(self, interaction: discord.Interaction):
        self.dmap.set_time()
        value = self.values[0]
        for option in self.options:
            option.default = option.value == value
        self.dmap.style = value
        await interaction.response.edit_message(view=self.view)
        await self.dmap.update()


class Settings(discord.ui.View):
    dmap: Map
    embed: discord.Embed

    def __init__(self, dmap: Map):
        super().__init__(timeout=600)
        self.dmap = dmap
        self.embed = discord.Embed(title="Settings")

        for item in [StyleSelect(dmap)]:
            self.add_item(item)

    async def send(self, response: discord.InteractionResponse):
        await response.send_message(embed=self.embed, view=self, ephemeral=True)

    async def _update_map(self, interaction):
        await interaction.response.defer()
        self.dmap.set_time()
        await self.dmap.update()

    async def __change_width(self, interaction, value):
        self.dmap.width += value
        await self._update_map(interaction)

    async def __change_height(self, interaction, value):
        self.dmap.height += value
        await self._update_map(interaction)

    @discord.ui.button(label="+ Width", row=2)
    async def inc_width(self, _, interaction: discord.Interaction):
        await self.__change_width(interaction, 50)

    @discord.ui.button(label="- Width", row=2)
    async def dec_width(self, _, interaction: discord.Interaction):
        await self.__change_width(interaction, -50)

    @discord.ui.button(label="+ Height", row=2)
    async def inc_height(self, _, interaction: discord.Interaction):
        await self.__change_height(interaction, 30)

    @discord.ui.button(label="- Height", row=2)
    async def dex_height(self, _, interaction: discord.Interaction):
        await self.__change_height(interaction, -30)
