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
                        if message.embeds == []: #only activates these if no embed is found
                            await message.clear_reactions() #clears out all the old reactions
                            await message.add_reaction('✅')
                            if channel.id == 838499217697013780: #later
                                await message.add_reaction('⏭️')
                                    #prompt to move to other channels
                            else:
                                await message.add_reaction('⏮️')
                                #prompt to move back to later

        await ctx.send('Audit of shopping lists complete!')
        print('audit complete')


#list command
@bot.command()
async def list(ctx):
    #space to comment out
    guild = bot.get_guild(838493859474440242) #our server
    channel = bot.get_channel(938883951848722493) #grocery list
    async for message in channel.history(limit=20): #deletes grocery list
        await message.delete()

    for cat, channels in guild.by_category():
        if cat.id == 838499351965859850: #shopping category
            for channel in channels:
                print('currently listing:')
                print(channel.name)
                stack=[]
                async for message in channel.history(limit=200):
                    content = message.content
                    stack.append(content)
                    stack.append('\n')
                msg = ''.join([str(i) for i in stack])
                print(msg)
                embed = discord.Embed(
                    title=channel,
                    description=msg,
                    color=discord.Color.orange(),
                    )
                channel = bot.get_channel(938883951848722493) #grocery list
                await channel.send(
                embed = embed,
                    )


    await ctx.send('Here is your grocery list!')


#add reactions to messages
#aside from later and
@bot.event
async def on_message(message):
    category = str(message.channel.category)
    channel = str(message.channel)
    if category == "shopping":
        #print(category)
        #print(channel)
        if message.embeds == []: #only activates these if no embed is found
            await message.add_reaction('✅')
            if channel == 'later':
                await message.add_reaction('⏭️') #prompt to embed
            else:
                await message.add_reaction('⏮️') #prompt to later


    await bot.process_commands(message)

#what to do when a person reacts
@bot.event
async def on_raw_reaction_add(payload):
    userid = payload.user_id
    #print(userid)
    #if user.bot:
    if userid == 858373439781601300: #won't do events if corgibot is the one reacting
        return

    id = int(payload.message_id)

    userid = payload.user_id

    channel = bot.get_channel(payload.channel_id)
    message = await channel.fetch_message(id)
    if message.embeds == []: #only copy whole contents if not an embed
        content = message.content
    else:
        content = embed.title
        print(content)

    if payload.emoji.name == '✅': #move to purchased
        if payload.channel_id != 858879163142111272: #purchased
            channel = bot.get_channel(858879163142111272)
            await channel.send(content)

    if payload.emoji.name == '⏮️': #move to later
        if payload.channel_id != 838499217697013780: #later channel
            channel = bot.get_channel(838499217697013780)
            await channel.send(content)

    if payload.emoji.name == '⏭️': #embed to send places
        embed = discord.Embed(
            title=content,
            description='list of stores here',
            color=discord.Color.orange(),
        )
        await channel.send(
        embed = embed,
        )
        return


    await message.delete()


#run token, in different file because of security
with open(r'./files/token.txt') as f:
    TOKEN = f.readline()

#this is for the token
bot.run(TOKEN)
