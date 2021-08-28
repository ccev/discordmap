from __future__ import annotations
import discord
from typing import TYPE_CHECKING

from config import AREAS

if TYPE_CHECKING:
    from map.map import Map


class AreaSelect(discord.ui.Select):
    def __init__(self, dmap: Map):
        super().__init__(custom_id="area", placeholder="Jump to an area", min_values=0, max_values=1, row=1)

        self.dmap = dmap
        for i, area in enumerate(AREAS):
            self.options.append(discord.SelectOption(
                label=area.name, description=f"Jump to {area.name}", value=str(i)
            ))

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer()
        if not self.dmap.is_author(interaction.user.id):
            return
        await self.dmap.start_load()
        value = int(self.values[0])
        self.dmap.jump_to_area(AREAS[value])
        await self.dmap.update()
