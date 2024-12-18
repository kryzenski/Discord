import discord
from discord.ext import commands
import youtube_dl
import asyncio
from collections import defaultdict

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# Global variables
song_votes = defaultdict(int)  # Dictionary to store song votes
queue = []
current_song = None

# Helper function to download and play songs
def play_next(ctx):
    global current_song
    if len(queue) > 0:
        current_song = queue.pop(0)
        voice_client = discord.utils.get(bot.voice_clients, guild=ctx.guild)
        source = discord.FFmpegPCMAudio(current_song)
        voice_client.play(source, after=lambda e: play_next(ctx))
    else:
        current_song = None

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

@bot.command()
async def play(ctx, url):
    global queue

    if ctx.author.voice is None:
        await ctx.send("You need to join a voice channel first!")
        return

    voice_channel = ctx.author.voice.channel
    voice_client = discord.utils.get(bot.voice_clients, guild=ctx.guild)

    if voice_client is None:
        await voice_channel.connect()
        voice_client = discord.utils.get(bot.voice_clients, guild=ctx.guild)

    ydl_opts = {
        'format': 'bestaudio/best',
        'noplaylist': True,
        'quiet': True
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        audio_url = info['url']
        title = info.get('title', 'Unknown')
        queue.append(audio_url)

        await ctx.send(f"Queued: {title}")

    if not voice_client.is_playing():
        play_next(ctx)

@bot.command()
async def pause(ctx):
    voice_client = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    if voice_client and voice_client.is_playing():
        voice_client.pause()
        await ctx.send("Music paused.")
    else:
        await ctx.send("No music is playing.")

@bot.command()
async def stop(ctx):
    global queue, current_song
    queue.clear()
    current_song = None

    voice_client = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    if voice_client and voice_client.is_playing():
        voice_client.stop()
        await ctx.send("Music stopped.")

@bot.command()
async def volume(ctx, volume: int):
    voice_client = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    if voice_client:
        voice_client.source = discord.PCMVolumeTransformer(voice_client.source)
        voice_client.source.volume = volume / 100
        await ctx.send(f"Volume set to {volume}%.")
    else:
        await ctx.send("Bot is not connected to a voice channel.")

@bot.command()
async def like(ctx):
    global current_song

    if current_song:
        song_votes[current_song] += 1
        await ctx.send("Your vote has been counted!")
    else:
        await ctx.send("No song is currently playing.")

@bot.command()
async def chart(ctx):
    if len(song_votes) == 0:
        await ctx.send("No votes have been recorded yet.")
        return

    sorted_songs = sorted(song_votes.items(), key=lambda x: x[1], reverse=True)
    chart_list = "\n".join([f"{i+1}. {song}: {votes} votes" for i, (song, votes) in enumerate(sorted_songs[:10])])
    await ctx.send(f"Top 10 Songs:\n{chart_list}")

@bot.command()
async def lyrics(ctx):
    await ctx.send("Lyrics feature is not yet implemented.")

bot.run("YOUR_DISCORD_BOT_TOKEN")
