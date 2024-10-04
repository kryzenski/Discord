# AURA DISCORD BOT

import discord
from discord.ext import commands

# Create a dictionary to store the users' points
aura_points = {}

# Define positive and negative reactions
positive_reactions = ['👍', '❤️', '😂', '🎉']
negative_reactions = ['👎', '😢', '😡']

# Create the bot
intents = discord.Intents.default()
intents.reactions = True
intents.messages = True
intents.guilds = True
intents.message_content = True  # Needed to access message content
intents.members = True  # Needed to track members and their points

bot = commands.Bot(command_prefix='!', intents=intents)

# Function to update points based on reactions
def update_aura_points(user, reaction, is_adding):
    if user not in aura_points:
        aura_points[user] = 0

    if reaction.emoji in positive_reactions:
        if is_adding:
            aura_points[user] += 1  # Increase points for positive reactions
        else:
            aura_points[user] -= 1  # Decrease points if the reaction is removed

    elif reaction.emoji in negative_reactions:
        if is_adding:
            aura_points[user] -= 1  # Decrease points for negative reactions
        else:
            aura_points[user] += 1  # Restore points if the negative reaction is removed

# Event to handle when a reaction is added
@bot.event
async def on_reaction_add(reaction, user):
    if reaction.message.author == user:
        return  # Prevent users from reacting to their own messages

    # Update the message author's aura points based on the reaction
    update_aura_points(reaction.message.author, reaction, is_adding=True)

    # Send a message in the channel to show the updated points (optional)
    await reaction.message.channel.send(f"{reaction.message.author.display_name} now has {aura_points[reaction.message.author]} aura points!")

# Event to handle when a reaction is removed
@bot.event
async def on_reaction_remove(reaction, user):
    if reaction.message.author == user:
        return  # Prevent users from reacting to their own messages

    # Update the message author's aura points based on the reaction removal
    update_aura_points(reaction.message.author, reaction, is_adding=False)

    # Send a message in the channel to show the updated points (optional)
    await reaction.message.channel.send(f"{reaction.message.author.display_name} now has {aura_points[reaction.message.author]} aura points!")

# Command to check a user's aura points
@bot.command(name="points")
async def check_points(ctx, member: discord.Member = None):
    member = member or ctx.author  # If no member is specified, default to the command sender
    points = aura_points.get(member, 0)  # Get the member's points or 0 if they have none
    await ctx.send(f"{member.display_name} has {points} aura points!")

# Command to display the leaderboard
@bot.command(name="leaderboard")
async def leaderboard(ctx):
    if not aura_points:
        await ctx.send("No aura points have been assigned yet.")
        return

    sorted_points = sorted(aura_points.items(), key=lambda item: item[1], reverse=True)
    leaderboard_message = "**Aura Points Leaderboard:**\n"
    for user, points in sorted_points:
        leaderboard_message += f"{user.display_name}: {points} points\n"

    await ctx.send(leaderboard_message)

# Run the bot with the token (replace 'YOUR_BOT_TOKEN' with your actual bot token)
bot.run('YOUR_DISCORD_BOT_TOKEN')
