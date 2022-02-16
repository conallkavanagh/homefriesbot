import discord
from discord.ext import commands
import random
import subprocess
import logging

description = '''An example bot to showcase the discord.ext.commands extension
module.

There are a number of utility commands being showcased here.'''

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix='?', description=description, intents=intents)

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

@bot.command()
async def add(ctx, left: int, right: int):
    """Adds two numbers together."""
    await ctx.send(left + right)

@bot.command()
async def roll(ctx, dice: str):
    """Rolls a dice in NdN format."""
    try:
        rolls, limit = map(int, dice.split('d'))
    except Exception:
        await ctx.send('Format has to be in NdN!')
        return

    result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))
    await ctx.send(result)

@bot.command(description='For when you wanna settle the score some other way')
async def choose(ctx, *choices: str):
    """Chooses between multiple choices."""
    await ctx.send(random.choice(choices))

@bot.command()
async def repeat(ctx, times: int, *, content='repeating...'):
    """Repeats a message multiple times."""
    for i in range(times):
        try:
            await ctx.send(content)
        except: KeyboardInterrupt

@bot.command()
async def stop(ctx):
    return KeyboardInterrupt

@bot.command()
async def joined(ctx, member: discord.Member):
    """Says when a member joined."""
    await ctx.send('{0.name} joined in {0.joined_at:}'.format(member))

@bot.group()
async def cool(ctx):
    """Says if a user is cool.

    In reality this just checks if a subcommand is being invoked.
    """
    if ctx.invoked_subcommand is None:
        await ctx.send('No, {0.subcommand_passed} is not cool'.format(ctx))

@cool.command(name='bot')
async def _bot(ctx):
    """Is the bot cool?"""
    await ctx.send('Yes, the bot is cool.')

@bot.command()
@commands.is_owner()
async def get_history_of_channel(ctx, num: int):
    channel = bot.get_channel(num)
    print(f"getting all messages from channel {channel.name}")

    with open(f'{channel.name}.txt', 'w') as f:
        async for message in channel.history(limit=None): # adding None lets us retrieve every message
            # add it to the quotes
            f.write(f"{message.content}\n\n")

@bot.command()
async def ping(ctx):
    await ctx.send(f'Pong! {bot.latency * 1000:.0f} ms')

@bot.command()
async def quote(ctx):
    with open('quote-quotes.txt', 'r') as f:
        quotes = f.read().rstrip().split('\n\n')
    await ctx.send(random.choice(quotes))

@bot.command()
async def big(ctx, *, message):
    result = subprocess.run(['figlet', message], capture_output=True, text=True).stdout
    await ctx.send(f'```\n{result}\n```')

@bot.command()
@commands.is_owner()
async def say(ctx, num: int, *, message):
    channel = bot.get_channel(num)
    await channel.send(message)

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.channel.id == 889502838890319892:
        with open('quote-quotes.txt', 'a') as f:
            f.write(f"{message.content}\n\n")

    await bot.process_commands(message)

bot.run('NO-LONGER-HERE')
