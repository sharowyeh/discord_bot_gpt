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
    logger.debug(f'bot is ready, user:{bot.user}')

@bot.event
async def on_message(message: discord.Message):
    logger.debug(f'on_message, author:{message.author} msg:{message.content}')
#    if message.author == bot.user:
#        logger.debug('on bot message something')

@bot.slash_command(name='echo', description='Just make sure bot is still alive')
@option('message', description='The message')
async def echo(ctx, message: str):
    logger.debug(f'echo msg:{message}')
    await ctx.respond(message)

@bot.slash_command(name='hello', description='Just let bot say hello world')
@option('text', description='Additional text')
async def hello(ctx, text: str=''):
    logger.debug(f'{ctx.author} hello world! {text}')
    await ctx.respond(f'{ctx.author} hello world! {text}')

@bot.slash_command(name='chat', description='Talk to GPT3')
@option('text', description='The text message')
@option('temp', description='Completion temperature')
async def chat(ctx, text: str, temp: float=0.5):
    """Talk to GPT3,
    :param text: The text message
    :param temp: Completion temperature
    """
    if temp < 0 or temp > 1 or round(temp, 1) != temp:
        temp = 0.5
    logger.debug(f'{ctx.author} text:{text} temp:{temp}')

    # reply message first for context prevent task terminated before openai response(I guess?)
    reply_text = f"{ctx.author} said '{text}'"
    msg = await ctx.respond(f"{reply_text}")

    # let openai API call by async? but completion does not have acreate method
    # or use from asgiref.sync import sync_to_async? [link](https://github.com/openai/openai-python/issues/98)
    token_length = 100
    #TODO: try catch here, you may need get exception from API rate limit!
    resp = openai.Completion.create(
        engine="text-davinci-003",
        prompt=text,
        temperature=temp,
        max_tokens=token_length,
#        frequency_penalty=0,
#        presence_penalty=0
#        stream=False,
#        stop="\n",
    )

    while True:
        print(resp)
        if not hasattr(resp, 'choices') or len(resp.choices) == 0:
            await ctx.send("I got no response")
            break
        if not resp.choices[0].text:
            await ctx.send("I got empty response")
            break
        print(f"choices: {resp.choices[0].text}")
        reply_text += resp.choices[0].text
        await msg.edit_original_response(content=f"{reply_text}")
        
        if not resp.choices[0].finish_reason or resp.choices[0].finish_reason != "length":
            print(f"Response may end")
            break;

        # append text for rest of responses(is necessary?)
        text += resp.choices[0].text
        # increase token length
        token_length += 100
        resp = openai.Completion.create(
            engine="text-davinci-003",
            prompt=text,
            temperature=temp,
            max_tokens=token_length,
#            stream=False,
#            stop="\n",
        )
    reply_text += "\n🤔"
    await msg.edit_original_response(content=f"{reply_text}")
    print("==== end of resp ====")

bot.run(os.environ.get('DISCORD_BOT_TOKEN'))
exit()
