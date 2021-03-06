from discord.ext import commands
import asyncio
import discord

from map.map import Map
import config

bot = commands.Bot("!", slash_command_guilds=config.GUILDS, slash_commands=True, intents=discord.Intents.none())
config.ICONSET = config.ICONSETS[0]


@bot.command(name="map", message_command=False)
async def map_command(ctx: commands.Context):
    """Show an interactive map"""
    wait_message = None
    if not config.EMOJIS:
        wait_message = await ctx.send("Still starting up. Give me a second")
    while not config.EMOJIS:
        await asyncio.sleep(1)
    if wait_message:
        await wait_message.delete()

    dmap = Map(ctx.author.id, ctx.bot.loop)
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
