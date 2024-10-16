import discord
from discord.ext import commands
import youtube_dl
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import asyncio

# Spotify API credentials
SPOTIPY_CLIENT_ID = 'your-spotify-client-id'
SPOTIPY_CLIENT_SECRET = 'your-spotify-client-secret'

# Discord bot token
DISCORD_TOKEN = 'your-discord-bot-token'

# Bot prefix
PREFIX = '!'

# Volume control
VOLUME = 0.5

# Song voting system
VOTES = {}

# Top 10 chart list
CHART = []

bot = commands.Bot(command_prefix=PREFIX)

# Spotify API setup
sp_client = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET))

# YouTube-DL setup
ydl_opts = {'format': 'bapest'}
ydl = youtube_dl.YoutubeDL(ydl_opts)

@bot.event
async def on_ready():
    print(f'BeatBot is online!')

@bot.command(name='play', help='Play a song from Spotify, YouTube, or a web link')
async def play(ctx, url: str):
    # Check if the song is from Spotify
    if 'spotify' in url:
        # Extract song ID from Spotify URL
        song_id = url.split('/')[-1]
        song = sp_client.track(song_id)
        title = song.name
        artist = song.artists[0].name
        url = song.preview_url
    # Check if the song is from YouTube
    elif 'youtube' in url:
        # Extract video ID from YouTube URL
        video_id = url.split('?v=')[-1]
        title = ydl.extract_info(f'https://www.youtube.com/watch?v={video_id}', download=False)['title']
        artist = ydl.extract_info(f'https://www.youtube.com/watch?v={video_id}', download=False)['uploader']
    # Play the song
    voice_channel = ctx.author.voice.channel
    voice_client = await voice_channel.connect()
    voice_client.play(discord.FFmpegPCMAudio(url), after=lambda e: print(f'Player error: {e}') if e else None)
    voice_client.source.volume = VOLUME
    await ctx.send(f'Now playing: {title} by {artist}')

@bot.command(name='pause', help='Pause the current song')
async def pause(ctx):
    voice_client = ctx.voice_client
    if voice_client.is_playing():
        voice_client.pause()
        await ctx.send('Song paused')
    else:
        await ctx.send('No song is playing')

@bot.command(name='stop', help='Stop the current song')
async def stop(ctx):
    voice_client = ctx.voice_client
    if voice_client.is_playing():
        voice_client.stop()
        await ctx.send('Song stopped')
    else:
        await ctx.send('No song is playing')

@bot.command(name='volume', help='Adjust the volume of the music bot')
async def volume(ctx, volume: int):
    global VOLUME
    VOLUME = volume / 100
    voice_client = ctx.voice_client
    if voice_client.is_playing():
        voice_client.source.volume = VOLUME
        await ctx.send(f'Volume set to {volume}%')
    else:
        await ctx.send('No song is playing')

@bot.command(name='like', help='Vote for the current song')
async def like(ctx):
    global VOTES
    song_title = ctx.voice_client.source.title
    if song_title in VOTES:
        VOTES[song_title] += 1
    else:
        VOTES[song_title] = 1
    await ctx.send(f'You liked {song_title}!')

@bot.command(name='chart', help='View the top 10 voted songs')
async def chart(ctx):
    global CHART
    CHART = sorted(VOTES.items(), key=lambda x: x[1], reverse=True)[:10]
    chart_str = ''
    for i, (song, votes) in enumerate(CHART):
        chart_str += f'{i+1}. {song} - {votes} votes\n'
    await ctx.send(f'Top 10 chart:\n{chart_str}')

@bot.command(name='lyrics', help='View the lyrics of the current song')
async def lyrics(ctx):
    song_title = ctx.voice_client.source.title
    # Use a lyrics API or database to fetch the lyrics
    lyrics = 'Lyrics not available'
    await ctx.send(f'Lyrics for {song_title}:\n{lyrics}')

bot.run(DISCORD_TOKEN)
