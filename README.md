NOTE: not sure is interactions-py or rpi issue, v4.3.x discord interactions usually freeze without response in period of time.

20230214: change to use py-cord works fine to me.

env=> python 3.8 or later version

- [py-cord](https://github.com/Pycord-Development/pycord/blob/master/examples/edits.py)
  - standalone module installation with own offical discord module dependency
  - ease of using slash_command to display bot commands description on discord client apps
  - v2.x for option class display parameter decorators in client app
  - python 3.8 is recommanded using py-cord v2.x and later version

- [interactions-py](https://github.com/interactions-py/interactions.py) for discord command dispatch
  - this package has python version dependency
  - python3.7(3.7.9 from my dev nb) or 3.6:
    - will always install discord.py obsoleted version 0.16.x
  - python3.10:
    - install the latest version of discord-py-interactions without discord.py dependency
  - python3.8:
    - not sure because been changed to use py-cord


# settings in discord #

discord developer [site](https://discord.com/developers/applications/)

fill-out app information and setup auth (can in-app auth)
 - bot, application.command
 - send message, embed links, add reactions
 - create auth url(using same permission)
 - go to link to auth for discord client app invite this bot
[optional] get client secret from the same page(can only renew for display)
 - if want to use programmable way to install bot automatically(perhaps? probably?)

[optional] get discord guild id(id for identify servers, channels or hashtags)
 - from discord client app, user settings-> advanced-> enable developer
 - right click from any of servers, channels or hashtags, get id from menu
 - leave guild id unset let bot interaction where invited in(seems that)
refer to https://interactionspy.readthedocs.io/en/latest/quickstart.html

export to env `DISCORD_BOT_TOKEN` for python packages
export to env `DEFAULT_GUILD_ID` if specific(its fine to leave unset)

# py-cord #

can be used mixed with offical discord.py, and 

slash_command helps bot command description automatically show up on client apps
- for message editing, refer to [example](https://github.com/Pycord-Development/pycord/blob/master/examples/edits.py)


# discord-py-interactions #

just following discord-py-interactions [quickstart](https://interactionspy.readthedocs.io/en/latest/quickstart.html)


# openai api #

openai related api recently manipulate from another [twitch bot project](https://github.com/sharowyeh/twitch-bot-gpt#openai-api) 

just make submodule to use updated completion behavior
```
> git clone --recursive-submodules `
```
or
```
> git submodule init
> git submodule update
```
and need
```
> pip install -r twitch_bot_gpt/requirements.txt
```

# for my raspberrypi env #

for py-cord v2.x, using python v3.8 

Cuz rpi OS is buster using python3.7.3, need to download python source code and rebuild it
`wget <new version tgz from python website>`
`tar -xzvf Pythonx.x.tgz`
`cd <to Pythonx.x>`
`./configure --enable-optimizations`
`[sudo] make altinstall`
the binaries will placed at /usr/local/bin or /home/pi/.local/bin

I don't want to break out OS default python3.7, so just create venv from new python binary
`/usr/local/bin/python3.x -m venv ".venv"`
`source .venv/bin/activate`
`source .myenv.sh` and failed if unset DEFAULT_GUILD_ID at first time

