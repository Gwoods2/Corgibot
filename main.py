import os
import discord
import random
import logging
from utils.ids import(
    GuildIDs,
    CategoryIDs,
    ChannelIDs,
    UserIDs,
)

from discord.ext import commands

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='.', intents=intents)

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)
"""
#these are up top because i need them in both on message and on reaction
storecount = 0
storeincrement = 0
stackstore = []
"""
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
        guild = bot.get_guild(GuildIDs.LG_SHOPPING)
        for cat, channels in guild.by_category():
            if cat.id == CategoryIDs.SHOPPING: #shopping
                for channel in channels:
                    print('currently auditing:')
                    print(channel.name)
                    print('-----')
                    async for message in channel.history(limit=200):
                        #only activates these if no embed is found
                        if message.embeds == []:
                            await message.clear_reactions() #clears out all the old reactions
                            await message.add_reaction('✅')
                            if channel.id == ChannelIDs.LATER: #later
                                await message.add_reaction('⏭️')
                                    #prompt to move to other channels
                            else:
                                await message.add_reaction('⏮️')
                                #prompt to move back to later
                        #cleans up embeds so i don't have to do it manually
                        else:
                            await message.delete()

        await ctx.send('Audit of shopping lists complete!')
        print('audit complete')


#list command
@bot.command()
async def list(ctx):
    #space to comment out
    guild = bot.get_guild(GuildIDs.LG_SHOPPING) #our server
    channel = bot.get_channel(ChannelIDs.GROCERY_LIST) #grocery list
    async for message in channel.history(limit=20): #deletes grocery list
        await message.delete()

    for cat, channels in guild.by_category():
        if cat.id == CategoryIDs.SHOPPING: #shopping category
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
                channel = bot.get_channel(ChannelIDs.GROCERY_LIST) #grocery list
                await channel.send(
                embed = embed,
                    )


    await ctx.send('Here is your grocery list!')




#what to do when a person reacts
@bot.event
async def on_raw_reaction_add(payload):
    userid = payload.user_id
    #print(userid)
    #if user.bot:
    if userid == UserIDs.SELF: #won't do events if corgibot is the one reacting
        return

    id = int(payload.message_id)

    userid = payload.user_id

    channel = bot.get_channel(payload.channel_id)
    message = await channel.fetch_message(id)
    #print(message)
    if message.embeds == []: #only copy whole contents if not an embed
        content = message.content
        #print(content)
    #else:
        #content = embed.title
        #print(content)

    if payload.emoji.name == '✅': #move to purchased
        if payload.channel_id != ChannelIDs.PURCHASED:
            channel = bot.get_channel(ChannelIDs.PURCHASED)
            await channel.send(content)
            #workaround to delete the message, needed after adding forward
            channel = bot.get_channel(payload.channel_id)
            #print(channel.name)
            message = await channel.fetch_message(payload.message_id)
            #print(message.content)
        await message.delete()
        return

    if payload.emoji.name == '⏮️': #move to later
        if payload.channel_id != ChannelIDs.LATER:
            channel = bot.get_channel(ChannelIDs.LATER)
            await channel.send(content)
            channel = bot.get_channel(payload.channel_id)
            message = await channel.fetch_message(payload.message_id)
        await message.delete()
        return

    if payload.emoji.name == '⏭️': #embed to send places
        stackstore = []
        storecount = 0
        storeincrement = 0
        storenumber = 0
        #stackemoji = []
        #fullstack = []
        #numberstore = ''
        guild = bot.get_guild(GuildIDs.LG_SHOPPING)
        for cat, channels in guild.by_category():
            if cat.id == CategoryIDs.SHOPPING: #shopping category
                for channel in channels:
        #for channel in CategoryIDs.SHOPPING:
                    if channel.id != ChannelIDs.LATER:
                        if channel.id != ChannelIDs.PURCHASED:

                            stackstore.append(channel.name)
                            storecount = storecount + 1
                            #print(storecount)
                            #print(stackstore)
        #sets up the referenced message to refer to later
        referenced = payload.message_id #do  i need this?
        #print(referenced)
        #sets up the embed
        embed = discord.Embed(
            title=content,
            color=discord.Color.orange(),
            #fields= [
            #{ name:name, value:value}
            #]
            )
        #opens the counting digits file
        #with open(r'./files/countingdigits.txt') as f:
            #for line in f:
            #    line = line.replace("\r", "").replace("\n", "")
            #alternates adding numbers and
        for x in stackstore:
            storenumber=storenumber+1
            numberstore = str(storenumber)
            #print(numberstore)
            embed.add_field(name="** **", value=numberstore+". "+x, inline=True)
            #print(x)
            #fullstack.append(f.readline())
            #fullstack.append(x)
            #fullstack.append('\n')
            #fullstack.append(f.readline()+':'+x+'\n')
            #print(fullstack)

        #embed.add_field(name='name', value='value', inline=true)
        #embed.add_field(name="** **", value=fullstack, inline=False)
        #print(fullstack)
        await message.reply(
        embed = embed,
        delete_after = 60
        #message = message
        )
        #routes reactions to the new embed
        #message = await channel.fetch_message(channel.last_message_id)
        #reacts to the embed with the emoji
        #with open(r'./files/countingemoji.txt') as g:
        """
        for x in stackstore:
            #reaction = g.readline()
            print(x)
            storeincrement=storeincrement+1
            if storeincrement == 1:
                await message.add_reaction('1️⃣') #try to add 1
        """

        return
    #sets up the list of store count emoji
    if [
    payload.emoji.name == '1️⃣' or
    payload.emoji.name == '2️⃣' or
    payload.emoji.name == '3️⃣' or
    payload.emoji.name == '4️⃣' or
    payload.emoji.name == '5️⃣' or
    payload.emoji.name == '6️⃣' or
    payload.emoji.name == '7️⃣' or
    payload.emoji.name == '8️⃣' or
    payload.emoji.name == '9️⃣' or
    payload.emoji.name == '0️⃣']:
        #a bunch of checks that can be commented out
        #print('payload emoji was a number') #tests whether the if statement worked
        messageid = payload.message_id
        #print('embed message id is '+str(messageid)) #check
        embedmes = await channel.fetch_message(payload.message_id)
        #print('embed message fetched')
        #print('embed message is '+str(embedmes)) #check
        #print('embed message embed is '+str(embedmes.embeds))
        referencedmes = message.reference
        #print('referencedmes 1: '+str(referencedmes))
        referencedmes = await channel.fetch_message(referencedmes.message_id)
        #print('referenced message is '+str(referencedmes)) #check
        #print('referenced message text is '+str(referencedmes.content)) #check
        #print(content)

        #delivers message content to correct channel
        storecount = 0
        guild = bot.get_guild(GuildIDs.LG_SHOPPING)
        for cat, channels in guild.by_category():
            if cat.id == CategoryIDs.SHOPPING: #shopping category
                for channel in channels:
                    #skips later and purchased
                    if channel.id != ChannelIDs.LATER:
                        if channel.id != ChannelIDs.PURCHASED:
                            #checks for internal mechanisms
                            #print('channel is '+str(channel)) #check
                            storecount = storecount + 1
                            #print('storecount is '+str(storecount))

                            #the logic for which list
                            if payload.emoji.name == '1️⃣':
                                if storecount == 1:
                                    #print('sending to '+str(channel)) #check
                                    #send to new channel
                                    await channel.send(referencedmes.content)
                                    #deletes embed message
                                    #await message.delete()
                                    #change channel back to later?
                                    channel = bot.get_channel(ChannelIDs.LATER)
                                    #print('now on #later')
                                    #print('channel name is '+str(channel.name))
                                    #print('channel id is '+str(channel.id))
                                    #delete both messages
                                    await channel.delete_messages([
                                    embedmes, referencedmes
                                    ])
                                    return
                            if payload.emoji.name == '2️⃣':
                                if storecount == 2:
                                    await channel.send(referencedmes.content)
                                    channel = bot.get_channel(ChannelIDs.LATER)
                                    await channel.delete_messages([
                                    embedmes, referencedmes
                                    ])
                                    return
                            if payload.emoji.name == '3️⃣':
                                if storecount == 3:
                                    await channel.send(referencedmes.content)
                                    channel = bot.get_channel(ChannelIDs.LATER)
                                    await channel.delete_messages([
                                    embedmes, referencedmes
                                    ])
                                    return
                            if payload.emoji.name == '4️⃣':
                                if storecount == 4:
                                    await channel.send(referencedmes.content)
                                    channel = bot.get_channel(ChannelIDs.LATER)
                                    await channel.delete_messages([
                                    embedmes, referencedmes
                                    ])
                                    return
                            if payload.emoji.name == '5️⃣':
                                if storecount == 5:
                                    await channel.send(referencedmes.content)
                                    channel = bot.get_channel(ChannelIDs.LATER)
                                    await channel.delete_messages([
                                    embedmes, referencedmes
                                    ])
                                    return
                            if payload.emoji.name == '6️⃣':
                                if storecount == 6:
                                    await channel.send(referencedmes.content)
                                    channel = bot.get_channel(ChannelIDs.LATER)
                                    await channel.delete_messages([
                                    embedmes, referencedmes
                                    ])
                                    return
                            if payload.emoji.name == '7️⃣':
                                if storecount == 7:
                                    await channel.send(referencedmes.content)
                                    channel = bot.get_channel(ChannelIDs.LATER)
                                    await channel.delete_messages([
                                    embedmes, referencedmes
                                    ])
                                    return
                            if payload.emoji.name == '8️⃣':
                                if storecount == 8:
                                    await channel.send(referencedmes.content)
                                    channel = bot.get_channel(ChannelIDs.LATER)
                                    await channel.delete_messages([
                                    embedmes, referencedmes
                                    ])
                                    return
                            if payload.emoji.name == '9️⃣':
                                if storecount == 9:
                                    await channel.send(referencedmes.content)
                                    channel = bot.get_channel(ChannelIDs.LATER)
                                    await channel.delete_messages([
                                    embedmes, referencedmes
                                    ])
                                    return
                            if payload.emoji.name == '0️⃣':
                                if storecount == 10:
                                    await channel.send(referencedmes.content)
                                    channel = bot.get_channel(ChannelIDs.LATER)
                                    await channel.delete_messages([
                                    embedmes, referencedmes
                                    ])
                                    return




        #return #skips deleting the embed while i test

    #await channel.fetch_message(id)
    #await message.delete()
    #await channel.delete_messages(id)

#add reactions to messages
@bot.event
async def on_message(message):
    category = str(message.channel.category)
    channel = str(message.channel)
    if category == "shopping":
        #only activates these if no embed is found
        if message.embeds == []:
            await message.add_reaction('✅')
            if channel == 'later':
                await message.add_reaction('⏭️') #prompt to embed
            else:
                await message.add_reaction('⏮️') #prompt to later
        #activates this with embeds
        else:
            #print('else') #check
            if channel == 'later':
                #print('later') #check
                #print(stackstore)
                stackstore = []
                storecount = 0
                storeincrement = 0
                #storenumber = 0
                #stackemoji = []
                #fullstack = []
                #numberstore = ''
                #copied from on react, because it wouldn't work without this
                guild = bot.get_guild(GuildIDs.LG_SHOPPING)
                for cat, channels in guild.by_category():
                    if cat.id == CategoryIDs.SHOPPING: #shopping category
                        for channel in channels:
                #for channel in CategoryIDs.SHOPPING:
                            if channel.id != ChannelIDs.LATER:
                                if channel.id != ChannelIDs.PURCHASED:

                                    stackstore.append(channel.name)
                                    storecount = storecount + 1
                for x in stackstore:
                    #reaction = g.readline()
                    #print(x) #check
                    #counter
                    storeincrement=storeincrement+1
                    #print(storeincrement) #check
                    #massive list of emoji
                    if storeincrement == 1:
                        await message.add_reaction('1️⃣')
                    if storeincrement == 2:
                        await message.add_reaction('2️⃣')
                    if storeincrement == 3:
                        await message.add_reaction('3️⃣')
                    if storeincrement == 4:
                        await message.add_reaction('4️⃣')
                    if storeincrement == 5:
                        await message.add_reaction('5️⃣')
                    if storeincrement == 6:
                        await message.add_reaction('6️⃣')
                    if storeincrement == 7:
                        await message.add_reaction('7️⃣')
                    if storeincrement == 8:
                        await message.add_reaction('8️⃣')
                    if storeincrement == 9:
                        await message.add_reaction('9️⃣')
                    if storeincrement == 10:
                        await message.add_reaction('0️⃣')

    await bot.process_commands(message)

#run token, in different file because of security
with open(r'./files/token.txt') as f:
    TOKEN = f.readline()

#this is for the token
bot.run(TOKEN)
