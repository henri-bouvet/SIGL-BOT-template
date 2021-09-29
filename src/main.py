import os
import random as Rand
from discord import Intents, Status, Permissions
from discord.ext import commands

bot = commands.Bot(
    intents=Intents.all(),
    command_prefix="!",  # Change to desired prefix
    case_insensitive=True  # Commands aren't case-sensitive
)

bot.author_id = 125185798575226880  # Change to your discord id!!!

@bot.event
async def on_ready():  # When the bot is ready
    print("I'm in")
    print(bot.user)  # Prints the bot's username and identifier

@bot.command()
async def name(ctx):
    await ctx.send(ctx.author.name)

@bot.command()
async def count(ctx):
    possible_status_pretty_print = [
        'Online: ',
        'Offline: ',
        'Idle: ',
        'Do not disturb: '
    ]

    possible_status = [
        Status.online,
        Status.offline,
        Status.idle,
        Status.do_not_disturb
    ]

    histo_members_status = [
        [],
        [],
        [],
        []
    ]

    output = ''

    for m in ctx.guild.members:
        histo_members_status[possible_status.index(m.status)].append(m)

    for i in range(4):
        output += possible_status_pretty_print[i]
        index = possible_status.index(possible_status[i])
        n = len(histo_members_status[index])
        output += str(n)

        if (n > 0):
            output += ' ('
            for j in range(0, n - 1):
                output += histo_members_status[index][j].name
                output += ', '
            output += histo_members_status[index][n - 1].name
            output += ')\n'
        else:
            output += '\n'

    await ctx.send(output)

def get_member_name(arg):
    return " ".join(arg)

@bot.command()
async def admin(ctx, *arg):
    member_name = get_member_name(arg)
    if (member_name == None or member_name == ''):
        await ctx.send('Missing parameter (member_name)')
        return

    member = None
    for m in ctx.guild.members:
        if m.name == member_name:
            member = m
            break

    if (member == None):
        await ctx.send('Not a server member')
        return

    admin_role = None
    for r in ctx.guild.roles:
        if r.name == 'Admin':
            admin_role = r

    if (admin_role == None):
        admin_role = await ctx.guild.create_role(
            name="Admin",
            permissions= Permissions(
                manage_channels = True,
                ban_members = True,
                kick_members = True
            )
        )

    await member.add_roles(admin_role)
    await ctx.send("The admin role was added to " + member_name)


@bot.command()
async def mute(ctx, *arg):
    member_name = get_member_name(arg)
    if (member_name == None or member_name == ''):
        await ctx.send('Missing parameter (member_name)')
        return

    member = None
    for m in ctx.guild.members:
        if m.name == member_name:
            member = m
            break

    if (member == None):
        await ctx.send('Not a server member')
        return

    ghost_role = None
    for r in ctx.guild.roles:
        if r.name == 'Ghost':
            ghost_role = r

    if (ghost_role == None):
        ghost_role = await ctx.guild.create_role(
            name='Ghost',
            permissions= Permissions(
                read_messages = False,
                send_messages = False,
                send_tts_messages = False,
                read_message_history = False
            )
        )

    for r in member.roles:
        if r.name == ghost_role.name:
            await member.remove_roles(ghost_role)
            await ctx.send("The Ghost role was removed from " + member_name)
            return

    await member.add_roles(ghost_role)
    await ctx.send("The Ghost role was added to " + member_name)

@bot.command()
async def ban(ctx, *arg):
    member_name = get_member_name(arg)
    if (member_name == None or member_name == ''):
        await ctx.send('Missing parameter (member_name)')
        return

    member = None
    for m in ctx.guild.members:
        if m.name == member_name:
            member = m
            break

    if (member == None):
        await ctx.send('Not a server member')
        return

    await ctx.guild.ban(member)
    await ctx.send(member_name + " was banned !!!")

@bot.command()
async def xkcd(ctx):
    random_number = Rand.randrange(1, 1000)
    await ctx.send('https://xkcd.com/' + str(random_number))

token = "<TOKEN>"
bot.run(token)  # Starts the bot