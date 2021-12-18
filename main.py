
import os, discord
import asyncio
from pynput import keyboard
from discord.ext import commands
from dotenv import load_dotenv
 
 
print("Discord - Load Opus:")
print(os.path.abspath("libopus.dll"))
b = discord.opus.load_opus(os.path.abspath("libopus.dll"))
print(b)
print("Discord - Is loaded:")
c = discord.opus.is_loaded()
print(c)

if not discord.opus.is_loaded():
    raise RunTimeError('Opus failed to load')

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='$')
vc = None

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

@bot.command()
async def test(ctx, arg):
    await ctx.send(arg)

@bot.command()
async def join(ctx):
    global vc
    try:
        channel = ctx.author.voice.channel
        if vc == None or not vc.is_connected():
            vc = await channel.connect()
    except AttributeError:
        print("Error: Is the user in a voice channel?")

async def play(file_name):
    if vc.is_playing():
        vc.stop()
    if vc.is_connected():
        vc.play(discord.FFmpegPCMAudio(executable=os.path.abspath("ffmpeg.exe"), source=os.path.abspath(file_name)))

@bot.command()
async def disconnect():
    if vc.is_connected():
        vc.disconnect()

def on_press(key):
    if key == keyboard.Key.f21:
        asyncio.run(play('saving15orless.mp3'))
    if key == keyboard.Key.f22:
        asyncio.run(play('letsgetyum.mp3'))
    if key == keyboard.Key.f23:
        asyncio.run(play('buttholebitch.mp3'))
    if key == keyboard.Key.f24:
        asyncio.run(play('1.wav'))

listener = keyboard.Listener(
    on_press=on_press)
listener.start()

bot.run(TOKEN)