from discord.ext import commands
import discord

from map.map import Map
import config

bot = commands.Bot(command_prefix="!", case_insensitive=1)


@bot.command()
async def map(ctx: discord.ext.commands.Context):
    dmap = Map(ctx.author.id)
    await dmap.send(ctx)


@bot.event
async def on_ready():
    if not config.EMOJIS:
        guild = await bot.fetch_guild(config.EMOJI_SERVER)
        emoji_names = ["mapDo", "mapUp", "mapLe", "mapRi", "mapBl", "mapPl", "mapMi",
                       "mapPo", "mapRa", "mapSt", "mapGy", "mapGr", "mapQu"]
        for emoji in guild.emojis:
            if emoji.name in emoji_names:
                config.EMOJIS[emoji.name] = str(emoji)
        print("ready")

bot.run(config.TOKEN)
