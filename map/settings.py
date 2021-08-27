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
