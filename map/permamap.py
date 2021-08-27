import discord
from map.map import Map


# unused because editing ephemerals locks the view
class PermaMap(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Open the map", custom_id="persistant:permamap", style=discord.ButtonStyle.blurple)
    async def open_map(self, _, interaction: discord.Interaction):
        dmap = Map()
        await dmap.set_map()
        await interaction.response.send_message(embed=dmap.embed, view=dmap, ephemeral=True)
