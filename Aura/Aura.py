# AURA DISCORD BOT

import discord
from discord.ext import commands

bot = commands.Bot(command_prefix='!')

# Dictionary to store user points
user_points = {}

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')

@bot.event
async def on_reaction_add(reaction, user):
    # Check if the reaction is on a message in a server channel
    if reaction.message.channel.type == discord.ChannelType.text:
        # Get the message author
        author = reaction.message.author
        # Check if the author is a server member
        if author in reaction.message.channel.guild.members:
            # Get the reaction emoji
            emoji = reaction.emoji
            # Check if the reaction is positive or negative
            if emoji in ['👍', '💯', '👏', '😂', '😎', '']:  # positive reactions
                points = 10
            elif emoji in ['❤️', '🔥', '😍', '💰']:  # Mega positive reactions
                points = 20
            if emoji in ['🏆', '⭐️', '👏']:  # Hyper positive reactions
                points = 10
            elif emoji in ['👎', '😠', '🚫','😢']:  # negative reactions
                points = -5
            else:
                return  # ignore other reactions
            # Update the user's points
            if author.id in user_points:
                user_points[author.id] += points
            else:
                user_points[author.id] = points
            # Send a message to the channel with the updated points
            await reaction.message.channel.send(f'{author.mention} now has {user_points[author.id]} AURA points!')

@bot.command(name='points')
async def get_points(ctx, user: discord.Member = None):
    if user is None:
        user = ctx.author
    if user.id in user_points:
        await ctx.send(f'{user.mention} has {user_points[user.id]} aura points!')
    else:
        await ctx.send(f'{user.mention} has 0 aura points!')

bot.run('YOUR_DISCORD_BOT_TOKEN')
