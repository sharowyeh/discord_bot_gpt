import os
import sys
import logging
import asyncio
import discord
from discord import option
from discord.ext import commands
import openai

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(logging.Formatter('[%(asctime)s] [%(levelname)s] %(name)s: %(message)s'))
logger.addHandler(handler)

if os.environ.get('DISCORD_BOT_TOKEN') is None:
    print('bot token can not be empty')
    exit()

if os.environ.get('OPENAI_API_KEY') is None:
    print('openai api key can not be empty')
    exit()

openai.api_key = os.environ.get('OPENAI_API_KEY')

intents = discord.Intents.all()

bot = commands.Bot(command_prefix='/', intents=intents)

@bot.event
async def on_ready():
    logger.debug('bot is ready')

@bot.event
async def on_message(message: discord.Message):
    logger.debug(f'on_message: {message.content}')
    if message.content.startswith('/arguments'):
        msg = await message.channel.send(f'Got arguments at event route:{message.content}')

@bot.slash_command(name='echo', description='Just make sure bot is still alive')
@option('message', description='The message')
async def echo(ctx, message: str):
    logger.debug(f'echo msg:{message}')
    await ctx.respond(message)

@bot.slash_command(name='arguments', description='The message with arguments')
@option('time', description='The milliseconds')
@option('message', description='The message')
async def arguments(ctx, time: int=1000, message: str=''):
    """Command with multiple arguments,
    :param time: The milliseconds
    :param message: The message
    """
    logger.debug(f'wait time:{time} msg:{message}')
    await ctx.respond(f'Got msg:{message} and wait:{time}')

#TODO: try to edit message in slash command respond

bot.run(os.environ.get('DISCORD_BOT_TOKEN'))
exit()

@bot.command()
@interactions.option()
async def chat_me(ctx: interactions.CommandContext, text: str):
    """talk something with open ai"""
    # reply message first for context prevent task terminated before openai response(I guess?)
    await ctx.send(f"said '{text}'")

    # let openai API call by async? but completion does not have acreate method
    # or use from asgiref.sync import sync_to_async? [link](https://github.com/openai/openai-python/issues/98)
    print(f"q: {text}")
    token_length = 100
    resp = openai.Completion.create(
        engine="text-davinci-003",
        prompt=text,
        temperature=0.5,
        max_tokens=token_length,
#        frequency_penalty=0,
#        presence_penalty=0
#        stream=False,
#        stop="\n",
    )
    reply_text = ""
    while True:
        print(resp)
        if not hasattr(resp, 'choices') or len(resp.choices) == 0:
            await ctx.send("I got no response")
            break
        if not resp.choices[0].text:
            await ctx.send("I got empty response")
            break
        reply_text = resp.choices[0].text
        print(f"a: {reply_text}")
        await ctx.send(f"{reply_text}")
        
        if not resp.choices[0].finish_reason or resp.choices[0].finish_reason != "length":
            print(f"Response may end")
            break;

        # append text for rest of responses(is necessary?)
        text += reply_text
        # increase token length
        token_length += 100
        resp = openai.Completion.create(
            engine="text-davinci-003",
            prompt=text,
            temperature=0.5,
            max_tokens=token_length,
#            stream=False,
#            stop="\n",
        )

    await ctx.send(f"hope I answered...")
    print("==== end of resp ====")

bot.start()
