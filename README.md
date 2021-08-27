# discordmap

An experimtenal Pokémon GO map using Discord components.

![demo](https://cdn.discordapp.com/attachments/523253670700122144/880930702051405905/vHkLFO0kUy.gif)

## Features
- Display Pokemon, Raids, Gyms, Pokestops and Grunts
- Pan & zoom
- Jump to areas
- variable multiplier to control how fast to pan/zoom

## Planned
- Only one user at a time 
- Have the map in an ephemeral
- Quests
- Settings to change iconsets, map styles, etc
- Filters
- RDM support

# Setup
- `cp config-example.py config.py` and fill out
- create a venv (important!) and `path/to/venv/pip install git+https://github.com/Rapptz/discord.py.git`
- Upload the emojis in the `emojis/` folder to your configured emoji server
- start the bot using `start_map.py`. You can get the map by saying `!map` wherever
