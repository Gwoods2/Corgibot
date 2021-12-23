import os
import discord
import random
import logging
#import corgi_token
#my_secret = os.environ['token']

from discord.ext import commands
#from corgi_token import token
#from keep_alive import keep_alive

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='.', intents=intents)

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.idle, activity=discord.Game('with their tail'))
    print('Corgibot Ready!')

@bot.command()
async def ping(ctx):
    await ctx.send(f'Pong! {round(bot.latency * 1000)}ms')

@bot.command()
async def clear(ctx, amount=5):
    await ctx.channel.purge(limit=amount)

@bot.command(aliases=['8ball'])
async def _8ball(ctx, *, question):
    responses = ['It is Certain.',
                'It is decidedly so.',
                'Without a doubt.',
                'Yes definitely.',
                'You may rely on it.',
                'As I see it, yes.',
                'Most likely.',
                'Outlook good.',
                'Yes.',
                'Signs point to yes.',
                'Reply hazy, try again.',
                'Ask again later.',
                'Better not tell you now.',
                'Cannot predict now.',
                'Concentrate and ask again.',
                "Don't count on it.",
                'My reply is no.',
                'My sources say no.',
                'Outlook not so good.',
                'Very doubtful.']
    await ctx.send(f'Question: {question}\nAnswer: {random.choice(responses)}')

#audit command
@bot.command()
async def audit(ctx):
    async with ctx.typing():
        guild = bot.get_guild(838493859474440242)
        for cat, channels in guild.by_category():
            if cat.id == 838499351965859850: #shopping
                for channel in channels:
                    print('currently auditing:')
                    print(channel.name)
                    print('-----')
                    async for message in channel.history(limit=200):
                        #print('message')
                        #print(message)
                        await message.add_reaction('✅')
                        await message.add_reaction('❌')
                        if channel.id == 838499217697013780:
                            await message.add_reaction('🇰') #kroger
                            await message.add_reaction('🇸') #sams
                            await message.add_reaction('🇲') #menards
                            await message.add_reaction('🇬') #walgreens
                            await message.add_reaction('🇼') #walmart
                            await message.add_reaction('🇯') #jungle-jims
        await ctx.send('Audit of shopping lists complete!')
        print('audit complete')

#add reactions to messages
#aside from later and
@bot.event
async def on_message(message):
    category = str(message.channel.category)
    channel = str(message.channel)
    if category == "shopping":
        #print(category)
        #print(channel)
        await message.add_reaction('✅')
        await message.add_reaction('❌')
        if channel == 'later' or channel == 'bot-testing-2':
            await message.add_reaction('🇰') #kroger
            await message.add_reaction('🇸') #sams
            await message.add_reaction('🇲') #menards
            await message.add_reaction('🇬') #walgreens
            await message.add_reaction('🇼') #walmart
            await message.add_reaction('🇯') #jungle-jims

    await bot.process_commands(message)

#what to do when a person reacts
@bot.event
async def on_raw_reaction_add(payload):
    userid = payload.user_id
    #print(userid)
    #if user.bot:
    if userid == 858373439781601300:
        return

    id = int(payload.message_id)

    userid = payload.user_id

    channel = bot.get_channel(payload.channel_id)
    message = await channel.fetch_message(id)
    content = message.content

    if payload.emoji.name == '✅':
        if payload.channel_id != 858879163142111272:
            #print('purchased')
            #print(id)
            channel = bot.get_channel(858879163142111272)
            await channel.send(content)

    if payload.emoji.name == '❌':
        if payload.channel_id != 838499217697013780:
            #print('later')
            #print(id)
            channel = bot.get_channel(838499217697013780)
            await channel.send(content)

    if payload.emoji.name == '🇰': #kroger
        channel = bot.get_channel(838493953183449128)
        await channel.send(content)

    if payload.emoji.name == '🇸': #sams
        channel = bot.get_channel(839559455834112030)
        await channel.send(content)

    if payload.emoji.name == '🇲': #menards
        channel = bot.get_channel(842194565586092062)
        await channel.send(content)

    if payload.emoji.name == '🇬': #walgreens
        channel = bot.get_channel(851887831394942976)
        await channel.send(content)

    if payload.emoji.name == '🇼': #walmart
        channel = bot.get_channel(858051070558076938)
        await channel.send(content)

    if payload.emoji.name == '🇯': # Jungle Jims
        channel = bot.get_channel(858084297725575228)
        await channel.send(content)


    await message.delete()


#run token, in different file because of security
with open(r'./files/token.txt') as f:
    TOKEN = f.readline()

#keep_alive()
#this is for the token
bot.run(TOKEN)
