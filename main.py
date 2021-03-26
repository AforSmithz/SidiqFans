import discord
import os
from discord.utils import get
from discord.ext import commands
from discord.ext.commands import cooldown, BucketType
import datetime
import pytz
from nyala import keep_alive
import random
from message_database import message_database

client = commands.Bot(command_prefix=["sidiq ", "siddick ", "sidick "])

#times
timezone = pytz.timezone('Asia/Jakarta')
enjing = timezone.localize(datetime.datetime(2002, 9, 26, 00, 00, 00))
siang = timezone.localize(datetime.datetime(2002, 9, 26, 11, 59, 00))
dalu = timezone.localize(datetime.datetime(2002, 9, 26, 17, 00, 00))
coolKasar = 0
coolSidiq = 0
#kosakata misuh
pisuhan = ['jancok', 'munyuk', 'bajingan', 'asu']

sidiq_id = os.getenv('SIDIQ')

messages_database = message_database()


@client.command()
async def pisuhi(ctx):
    now = datetime.datetime.now(timezone)
    if (now.time() > dalu.time()):
        mentions = []
        mentions.extend(ctx.message.mentions)
        mentions.extend(ctx.message.role_mentions)
        for i in mentions:
            misuh = random.choice(pisuhan)
            if (isinstance(i, discord.role.Role)):
                await ctx.send(f'{misuh} koe <@&{i.id}>')
                continue
            await ctx.send(f'{misuh} koe <@{i.id}>')


@client.command()
@cooldown(rate=2, per=60, type=BucketType.channel)
async def mode(ctx, mode):
    now = datetime.datetime.now(timezone)
    now_time = 'enjing' if enjing.time() <= now.time() <= siang.time() else (
        'siang' if enjing.time() <= now.time() <= siang.time() else 'dalu')
    modes = {
        'alus': f'Assalamualaikum Wr.Wb., sugeng {now_time} nami kula sidick',
        'kasar': 'Jancok kabeh'
    }
    await ctx.send(modes[mode.lower()])


@client.command(aliases=['r'])
async def resend(ctx, num=1):
    try:
        index = int(num)
    except Exception:
        index = 1
    print(index)
    server = str(ctx.message.guild)
    channel = str(ctx.message.channel)
    sent = messages_database.get(guild=server, channel=channel, depth=index)
    print(messages_database.get(server, channel, 2))
    for messages in sent:
        name = messages['author']
        message_text = messages['message']
        try:
            attachment = messages['attachments'][0]
            await ctx.send(
                f'<@{name}> ngirim {message_text}\n {attachment.proxy_url}\n')
        except Exception as e:
            await ctx.send(f'<@{name}> ngirim {message_text}\n ')
            print(e)


@client.event
async def on_ready():
    print('Hello nama gue sidiq salam kenal')


@client.listen('on_message')
async def sidick_reaction(message):

    now = datetime.datetime.now(timezone)

    #stickers
    pki = get(client.emojis, name='sidiqpki')
    oppa = get(client.emojis, name='sidiqoppa')
    makanbang = get(client.emojis, name='sidiqmakanbang')
    ngefak = get(client.emojis, name='sidiqngefak')

    if (message.author.id == int(sidiq_id)):
        global coolSidiq
        coolSidiq += 1

        if (coolSidiq == 5):
            global coolSidiqTime
            coolSidiqTime = now

        if (coolSidiq > 5):
            # Create datetime objects for each time (a and b)
            dateTimeA = datetime.datetime.combine(datetime.date.today(),
                                                  coolSidiqTime.time())
            dateTimeB = datetime.datetime.combine(datetime.date.today(),
                                                  now.time())
            # Get the difference between datetimes (as timedelta)
            dateTimeDifference = dateTimeB - dateTimeA
            # Divide difference in seconds by number of seconds in hour (3600)
            dateTimeDifferenceInSeconds = dateTimeDifference.total_seconds()

            if (dateTimeDifferenceInSeconds > 60.0):
                coolSidiq = 0

        if (coolSidiq <= 5):
            await message.add_reaction(pki)
            await message.add_reaction(oppa)
            await message.add_reaction(makanbang)
            await message.add_reaction(ngefak)
            await message.add_reaction('🇸')
            await message.add_reaction('🇮')
            await message.add_reaction('🇩')
            await message.add_reaction('ℹ️')
            await message.add_reaction('🇨')
            await message.add_reaction('🇰')


@client.listen('on_message')
async def sidick_kasar(message):
    global coolKasar

    #sidiq aliases
    sidiq = ("sidiq", "siddick", "sidick")

    #stiker
    ngefak = get(client.emojis, name='sidiqngefak')

    #now
    now = datetime.datetime.now(timezone)
    if (coolKasar == 2):
        global coolKasarTime
        coolKasarTime = now

    if (coolKasar > 2):
        # Create datetime objects for each time (a and b)
        dateTimeA = datetime.datetime.combine(datetime.date.today(),
                                              coolKasarTime.time())
        dateTimeB = datetime.datetime.combine(datetime.date.today(),
                                              now.time())
        # Get the difference between datetimes (as timedelta)
        dateTimeDifference = dateTimeB - dateTimeA
        # Divide difference in seconds by number of seconds in hour (3600)
        dateTimeDifferenceInSeconds = dateTimeDifference.total_seconds()

        if (dateTimeDifferenceInSeconds > 15.0):
            coolKasar = 0

    if (now.time() >= dalu.time() and coolKasar <= 2):
        if (client.user.mentioned_in(message)):
            coolKasar += 1
            await message.channel.send('rasah ngetag-ngetag')

        if (f'<@!{sidiq_id}>' in message.content
                or f'<@{sidiq_id}>' in message.content):
            coolKasar += 1
            await message.add_reaction(ngefak)
            await message.channel.send('rasah ngetag-ngetag')

        if (message.content in sidiq):
            await message.channel.send('opo nyuk')


@client.listen('on_message')
async def message_history(message):

    #channel
    channel = str(message.channel)

    #server
    server = str(message.guild)

    new_message = {
        'author': message.author.id,
        'message': message.content,
        'attachments': message.attachments
    }

    if (message.author == client.user):
        return

    messages_database.insert(server, channel, new_message)


@client.event
async def on_guild_join(guild):
    lobby = client.get_channel(int(os.getenv('CHANNEL')))
    await lobby.send('salken gue siddick @everyone')


# fungsi jahad
#@client.event
#async def on_message_delete(message):
#  await message.channel.send(f'{message.author.name} ngunsent ||{message.content}||')

keep_alive()
client.run(os.getenv('TOKEN'))
