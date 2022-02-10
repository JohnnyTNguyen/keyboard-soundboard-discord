
import os, sys, discord, random
import logging
import configparser
import asyncio
from pynput import keyboard
from discord.ext import commands
from dotenv import load_dotenv

ffmpeg_path = os.path.abspath("ffmpeg.exe")
settings_path = os.path.abspath("settings.ini")
discord_token_path = os.path.abspath("discordToken")

with open(discord_token_path, 'r') as f:
    discord_token = f.read()

config_file = configparser.ConfigParser()
config_file.sections()

if hasattr(sys, "_MEIPASS"):
    ffmpeg_path = os.path.join(sys._MEIPASS, "ffmpeg.exe")

config_file.read(settings_path)
if config_file.has_section("KEYMAPPINGS"):
    print("Config read successfully.")

# print("Discord - Load Opus:")
# print(os.path.abspath("libopus.dll"))
b = discord.opus.load_opus(os.path.abspath("libopus.dll"))
# print(b)
# print("Discord - Is loaded:")
c = discord.opus.is_loaded()
# print(c)

if not discord.opus.is_loaded():
    raise RunTimeError('Opus failed to load')

load_dotenv()
# TOKEN = os.getenv('DISCORD_TOKEN')

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

@bot.command()
async def reassign(ctx, key, file):
    try:
        config_file['KEYMAPPINGS'][key] = file
        with open('settings.ini', 'w') as newconfig:
            config_file.write(newconfig)
        await ctx.send('Remapped key ' + key + ' to ' + file)
    except:
        logging.exception("message")
        print('Error: Could not reassign key ' + key + ' to ' + file)

@bot.command()
async def clear(ctx, key):
    try:
        config_file['KEYMAPPINGS'].pop(key, None)
        with open('settings.ini', 'w') as newconfig:
            config_file.write(newconfig)
        await ctx.send('Cleared key ' + key)
    except:
        logging.exception("message")
        print('Error: Could not clear key ' + key)

async def play(file_name):
    if vc.is_playing():
        vc.stop()
    if vc.is_connected():
        vc.play(discord.FFmpegPCMAudio(executable=ffmpeg_path, source=file_name))

@bot.command()
async def disconnect(ctx):
    if vc.is_connected():
        await vc.disconnect()

@bot.command()
async def rando(ctx):
    # pick a random number
    # pick a random file from a directory
    try:
        # print(key)
        random_file = random.choice(os.listdir('sounds/'))
        print('sounds/' + random_file)
        sound_path = os.path.abspath('sounds/' + random_file)
        asyncio.run(await play(sound_path))
    except:
        # logging.exception("message")
        # print('No key or file found.')
        pass

def on_press(key):
    try:
        # print(key)
        print('sounds/' + config_file['KEYMAPPINGS'][str(key)])
        sound_path = os.path.abspath('sounds/' + config_file['KEYMAPPINGS'][str(key)])
        asyncio.run(play(sound_path))
    except:
        # logging.exception("message")
        # print('No key or file found.')
        pass

listener = keyboard.Listener(
    on_press=on_press)
listener.start()

# print("disc token: " + discord_token)
bot.run(discord_token)