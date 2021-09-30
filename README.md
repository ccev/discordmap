# discordmap

An experimtenal Pokémon GO map using Discord components.

![demo](https://cdn.discordapp.com/attachments/523253670700122144/880930702051405905/vHkLFO0kUy.gif)

## Features
- Display Pokemon, Raids, Gyms, Pokestops, Quests and Grunts
- Pan & zoom
- Jump to areas
- variable multiplier to control how fast to pan/zoom
- Settings to adjust map style, size and icon sets/size

## Planned
- Filters
- Themes
- save user settings across sessions
- Option to display current objects in a list. with details

# Setup
- `cp config-example.py config.py` and fill out
- create a venv (important!) and `path/to/venv/pip install git+https://github.com/iDevision/enhanced-discord.py.git aiomysql requests`
- Upload the emojis in the `emojis/` folder to your configured emoji server
- start the bot using `start_map.py`. You can get the map by saying `!map` wherever
