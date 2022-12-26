import os
import interactions
import openai

if os.environ.get('DISCORD_BOT_TOKEN') is None:
    print('bot token can not be empty')
    exit()

if os.environ.get('OPENAI_API_KEY') is None:
    print('openai api key can not be empty')
    exit()

openai.api_key = os.environ.get('OPENAI_API_KEY')

# given bot token from developer site bot page(can only renew for display)
# can leave unset guild id to the default_scope,
# that discord client app no need to enable developer mode as well...
# let bot interaction where invited in(perhaps? probably?)
bot = interactions.Client(
    token=os.environ.get('DISCORD_BOT_TOKEN'),
)

if os.environ.get('DEFAULT_GUILD_ID') is None:
    print('use token default scope')
else:
    # I need method to change client params
    bot = interactions.Client(
        token=os.environ.get('DISCORD_BOT_TOKEN'),
        default_scope=os.environ.get('DEFAULT_GUILD_ID'),
    )

#@bot.command(
#    name="say_hello",
#    description="let bot say hello world for debug",
#)
# can simplify as below
@bot.command()
async def say_hello(ctx: interactions.CommandContext):
    """let bot say hello world for debug"""
    await ctx.send("hello world")

@bot.command()
@interactions.option()
async def echo_me(ctx: interactions.CommandContext, text: str):
    """let bot echo your input"""
    await ctx.send(f"reply: '{text}'")

@bot.command()
@interactions.option()
async def chat_me(ctx: interactions.CommandContext, text: str):
    """talk something with open ai"""
    # use async? but completion does not have acreate method
    # or use from asgiref.sync import sync_to_async? [link](https://github.com/openai/openai-python/issues/98)
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=text,
        temperature=0.7,
        max_tokens=256,
#        frequency_penalty=0,
#        presence_penalty=0
    )
    print(response)
    reply_text = ""
    if hasattr(response, 'choices') and len(response.choices) > 0:
        reply_text = response.choices[0].text
    else:
        reply_text = "I can't understand what you say..."
    await ctx.send(f"{reply_text}")

bot.start()
