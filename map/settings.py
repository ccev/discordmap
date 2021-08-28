from __future__ import annotations
from typing import TYPE_CHECKING, Optional
import discord
from map.config import Icons
import config

if TYPE_CHECKING:
    from map.map import Map


class StyleSelect(discord.ui.Select):
    def __init__(self, dmap: Map, settings: Settings):
        super().__init__(custom_id="styleselect",
                         placeholder="Choose a map style",
                         min_values=0,
                         max_values=1,
                         row=0)
        for i, (style_name, style_value) in enumerate(config.STYLES):
            style_name = "Map Style: " + style_name
            self.options.append(discord.SelectOption(label=style_name, value=style_value, default=i == 0))
        self.dmap = dmap
        self.settings = settings

    async def callback(self, interaction: discord.Interaction):
        await self.dmap.start_load()
        value = self.values[0]
        for option in self.options:
            if option.value == value:
                option.default = True
                self.dmap.style_name = option.label.replace("Map Style: ", "")
            else:
                option.default = False
        self.dmap.style = value
        await self.settings.edit(interaction.response)
        await self.dmap.update()


class IconSelect(discord.ui.Select):
    def __init__(self, dmap: Map, settings: Settings):
        super().__init__(custom_id="iconselect",
                         placeholder="Choose an iconset",
                         min_values=0,
                         max_values=1,
                         row=1)
        for i, iconset in enumerate(config.ICONSETS):
            self.options.append(discord.SelectOption(label=iconset.name, value=str(i), default=i == 0))
        self.dmap = dmap
        self.settings = settings

    async def callback(self, interaction: discord.Interaction):
        await self.dmap.start_load()
        value = int(self.values[0])
        config.ICONSET = config.ICONSETS[value]
        for option in self.options:
            option.default = int(option.value) == value
        await self.settings.edit(interaction.response)
        await self.dmap.update()


class Settings(discord.ui.View):
    dmap: Map
    embed: discord.Embed

    def __init__(self, dmap: Map):
        super().__init__(timeout=600)
        self.dmap = dmap
        self.make_embed()

        for item in [StyleSelect(dmap, self), IconSelect(dmap, self)]:
            self.add_item(item)

    async def send(self, response: discord.InteractionResponse):
        await response.send_message(embed=self.embed, view=self, ephemeral=True)

    async def edit(self, response: discord.InteractionResponse):
        self.make_embed()
        await response.edit_message(embed=self.embed, view=self)

    def make_embed(self):
        text = (
            f"Map Style: **{self.dmap.style_name}**\n"
            f"Icons: **{config.ICONSET.name}**\n"
            f"Map size: **{self.dmap.width}x{self.dmap.height}px**"
        )
        self.embed = discord.Embed(title="Settings", description=text)
        self.embed.set_footer(text='When you\'re done here, click "Dismiss message" below')

    async def _update_map(self, interaction):
        await self.edit(interaction.response)
        await self.dmap.start_load()
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
